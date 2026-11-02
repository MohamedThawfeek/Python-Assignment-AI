import json


def products_lists(file_name="overall_product.json"):
    products = []
    categories = [file_name]

    for filename in categories:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            products.extend(data)

    product_list = [
        {
            "name": product["name"],
            "category": product["category"]
        }
        for product in products
    ]

    return products, product_list

def moderation_function(client, Options, messages, model="gpt-oss:120b"):
    response= client.chat(model,messages=messages, think=False, format="json", options=Options(temperature=0))
    check_vilation = response.message.content
    token_dict = {
        "prompt_tokens": response.prompt_eval_count or 0,
        "completion_tokens": response.eval_count or 0,
        "total_tokens": ((response.prompt_eval_count or 0)+ (response.eval_count or 0))

    }
    return json.loads(check_vilation), token_dict

def get_completion_from_messages(client, Options, messages, model="gpt-oss:120b", temperature=0, max_tokens=500):
    response= client.chat(model,messages=messages, think="low", options=Options(temperature=temperature))
    content = response.message.content
    token_dict = {
        "prompt_tokens": response.prompt_eval_count or 0,
        "completion_tokens": response.eval_count or 0,
        "total_tokens": ((response.prompt_eval_count or 0)+ (response.eval_count or 0))

    }
    return content, token_dict

def check_agent_final_response(client, Options, messages, model="gpt-oss:120b", temperature=0, max_tokens=500):
    response= client.chat(model,messages=messages, think="low", options=Options(temperature=temperature))
    content = response.message.content
    token_dict = {
        "prompt_tokens": response.prompt_eval_count or 0,
        "completion_tokens": response.eval_count or 0,
        "total_tokens": ((response.prompt_eval_count or 0)+ (response.eval_count or 0))

    }
    return content, token_dict



