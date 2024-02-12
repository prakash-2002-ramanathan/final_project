import requests


def call_voice(number):
    url = "https://api.bland.ai/v1/calls"

    task_des="As the all-knowing farm-related assistant at farmassist.org, your primary responsibility is to provide comprehensive and accurate assistance to callers seeking guidance and information related to farming. This entails possessing deep knowledge across various facets of agriculture, including crop cultivation, livestock management, pest control, soil health, irrigation techniques, and more. When a caller reaches out with a query, your role is to understand their specific needs and concerns, and then offer relevant advice, solutions, or resources to address their issue effectively. This could involve recommending specific farming practices, suggesting suitable crop varieties or animal breeds, advising on pest management strategies, providing tips for optimizing yields, or offering insights into sustainable farming methods. Your goal is to be a trusted source of expertise and support for farmers, helping them overcome challenges, improve productivity, and achieve success in their agricultural endeavors. By leveraging your extensive knowledge and expertise, you aim to empower farmers with the information and guidance they need to thrive in their profession and contribute to the sustainable growth of the agricultural industry."

    payload = {
        "phone_number": number,
        "task": task_des,
        "model": "turbo",
        "answered_by_enabled": False,
        "reduce_latency": True,
        "voice_id": 2,
        "wait_for_greeting": True,
        "first_sentence": "Hello mate how is it going?",
        "record": True,
        "language": "eng",
        "max_duration": 10,
        "amd": False,
        "request_data":{},
        "voice_settings":{
            "speed": 1
        },
        "answered_by_enabled": False
    }
    headers = {
        "authorization": "sk-pakk9mxnnf9qf6jpuzh0lxoqeve6yi23g00kg349kheceobcp4zlxgq61qepp2qh69",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)