import json
import urllib.request
import urllib.parse
import sys
import time

# 测试用的一个简单 ComfyUI 工作流，只包含我们修改的加载器和处理器
# 我们需要向本地模型发起请求（因为可能没有 API Key），由于没有Key，它可能会返回 Error，
# 但为了验证 UI 格式，只要看 error 结构或正常响应是否包含 `ui` 参数。
# 注意我们手动传入一些测试参数

workflow = {
  "1": {
    "inputs": {
      "provider": "Custom/自定义",
      "model": "foo",
      "api_key": "YOUR_API_KEY", # 替换为您想要测试的真实 KEY 或者随便乱填以产生报错
      "custom_base_url": "http://example.com"
    },
    "class_type": "LLM_Loader"
  },
  "2": {
    "inputs": {
      "system_prompt": "你是一个AI大模型",
      "prompt": "你好",
      "prep_img": "",
      "temperature": 0.7,
      "seed": 0,
      "llm_config": [
        "1",
        0
      ]
    },
    "class_type": "OpenAICompatibleLoader"
  },
  "3": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "4",
        0
      ]
    },
    "class_type": "SaveImage"
  },
  "4": {
    "inputs": {
        "image": "example.png"
    },
    "class_type": "LoadImage"
  }
}


def queue_prompt(prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    req =  urllib.request.Request("http://127.0.0.1:8188/prompt", data=data)
    return json.loads(urllib.request.urlopen(req).read())


def get_history(prompt_id):
    with urllib.request.urlopen("http://127.0.0.1:8188/history/{}".format(prompt_id)) as response:
        return json.loads(response.read())


def test():
    try:
        print("Submitting workflow to ComfyUI...")
        response = queue_prompt(workflow)
        prompt_id = response['prompt_id']
        print(f"Submitted! Prompt ID: {prompt_id}")
        
        while True:
            history = get_history(prompt_id)
            if prompt_id in history:
                print("\nExecution finished!")
                result = history[prompt_id]
                
                # Check for UI data in node '2'
                outputs = result.get('outputs', {})
                if '2' in outputs:
                    node_2_output = outputs['2']
                    if 'ui' in node_2_output:
                        print("✅ Success! 'ui' attribute found in response:")
                        print(json.dumps(node_2_output['ui'], indent=2, ensure_ascii=False))
                    else:
                        print("❌ Failed! No 'ui' attribute found in response:")
                        print(json.dumps(node_2_output, indent=2, ensure_ascii=False))
                break
            
            time.sleep(1)
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='replace')
        print(f"HTTP Error {e.code}:\n{error_body}")
    except Exception as e:
        print(f"Test failed (is ComfyUI running?): {e}")

if __name__ == "__main__":
    test()
