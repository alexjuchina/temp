# coding=utf-8
# b5
import gitlab
import openai
from flask import Flask, request
import json

# 设置你的GitLab和OpenAI的API凭据
gitlab_url = 'https://git.gitlab-devops.com'
gitlab_token = 'Gc8ZjMxFyNo_Wy9NHZXo'
openai_api_key = 'sk-oVuRgPNKIcHCQlWNrPapIc4iyI2Dn2W0kTFb8EKK5bthGQbj'

# 连接到GitLab
gl = gitlab.Gitlab(gitlab_url, private_token=gitlab_token)

# 连接到OpenAI
openai.api_key = openai_api_key
openai.base_url = "https://api.chatanywhere.com.cn"

# 监听GitLab项目中的Merge Request活动
def listen_to_mr_activity(project_id):
    project = gl.projects.get(project_id)
    # 在这里设置GitLab事件监听器，当MR新增note时触发相应的操作
    # 这里可以使用GitLab API中的Webhooks或者实时事件流来监听MR活动，具体实现取决于GitLab API的使用方式

# 处理新增的note
def handle_new_note(note):
    if '@ai' in note.body:
        # 提取问题内容
        question = extract_question_from_note(note.body)
        # 获取历史对话
        history = get_history_for_note(note)
        # 调用ChatGPT模型生成回复
        reply = generate_reply(question, history)
        # 将回复发送回GitLab项目中的相应MR
        post_reply_to_mr(note, reply)

# 从note中提取问题内容
def extract_question_from_note(note_body):
    # 这里可以使用自然语言处理技术（如正则表达式或者自然语言处理库）来提取问题内容
    # 例如，可以查找问句关键词，或者使用NLP库来识别问题类型
    # 这里是一个简单的示例，假设问题是note内容中以"问题："开头的部分
    question_start_index = note_body.find("问题：")
    if question_start_index != -1:
        question = note_body[question_start_index + len("问题："):]
        return question.strip()
    else:
        return "未找到问题内容"

# 获取历史对话
def get_history_for_note(note):
    # 这里可以使用GitLab API来获取MR中的历史对话
    # 例如，可以获取MR中所有的note，并根据需要整合历史对话
    # 这里是一个简单的示例，假设直接将MR中所有的note内容作为历史对话
    history = ""
    notes = note.mr.notes.list()
    for n in notes:
        history += n.body + "\n"
    return history

# 调用ChatGPT模型生成回复
def generate_reply(question, history):
    # 在这里调用OpenAI的ChatGPT模型生成回复
    # 你需要使用OpenAI的API来调用ChatGPT模型，传递问题和历史对话作为输入，获取生成的回复
    # 这里是一个简单的示例，假设直接使用OpenAI GPT-3 API来生成回复
    messages = [
        {"role": "system",
        "content": "你是一位资深编程专家，负责代码变更的审查工作。当用户在 GitLab MR 合并请求的 Notes中提及你的时候，你需要回答他们的问题。"
        },
        {"role": "user",
        "content": history + "问题：" + question,
        },
    ]
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response.choices[0].message.content.replace('\n\n', '\n')

# 将回复发送回GitLab项目中的相应MR
def post_reply_to_mr(note, reply):
    # 这里可以使用GitLab API来将回复发送回MR中
    # 例如，可以在MR中新增一个note，将生成的回复作为内容
    note.mr.notes.create({'body': reply})


app = Flask(__name__)

@app.route('/note', methods=['POST'])

def webhook():
    data = json.loads(request.data)

    # 解析JSON对象获取必要的参数
    gitlab_private_token = "x"
    project_id = data['project']['id']
    merge_request_id = data['object_attributes']['iid']
    merge_request_state = data['object_attributes']['state']
    openai_api_key = "sk-x"
    
    # 执行AI代码评审
    if merge_request_state == 'opened':
        ai_code_review(gitlab_private_token, project_id, merge_request_id, openai_api_key)
        return 'OK'
    else:
        return 'MR is closed, skip review.'
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)

# 主程序
if __name__ == "__main__":
    project_id = "YOUR_PROJECT_ID"
    listen_to_mr_activity(project_id)
