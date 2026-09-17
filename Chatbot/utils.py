import json
from collections import defaultdict
import openai

key="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"


openai.api_key = key

# Call Chat GPT API
def get_completion_from_messages(messages, model="gpt-4o-mini", temperature=0.2, max_tokens=500):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, 
    )
    return response.choices[0].message["content"]

# Categories Path
categories_file = 'categories.json'

# Create Categories File
def create_categories():
    categories_dict = {
      'Billing': [
                'Unsubscribe or upgrade',
                'Add a payment method',
                'Explanation for charge',
                'Dispute a charge'],
      'Technical Support':[
                'General troubleshooting'
                'Device compatibility',
                'Software updates'],
      'Account Management':[
                'Password reset'
                'Update personal information',
                'Close account',
                'Account security'],
      'General Inquiry':[
                'Product information'
                'Pricing',
                'Feedback',
                'Speak to a human']
    }
    
    with open(categories_file, 'w') as file:
        json.dump(categories_dict, file)
        
    return categories_dict

# Read the Create Categories
def get_categories():
    with open(categories_file, 'r') as file:
            categories = json.load(file)
    return categories

# Products Path
audio_equipment_file = 'Audio_equipment.json'
camera_file = 'Camera.json'
computer_products_file = 'computer_products.json'
gaming_consoles_file = 'Gaming_consoles.json'
mobile_file = 'mobile.json'
television_file = 'television.json'

# Combained all the product file path
all_items_files = [audio_equipment_file, camera_file, computer_products_file, gaming_consoles_file, mobile_file, television_file]

# Combained all the product is one file get categories and category items nested array 
def get_products():
    all_products = []
    categories = []
    category_items = []

    for file_path in all_items_files:

        with open(file_path, "r") as file:
            products = json.load(file)

        # Convert dict -> list
        if isinstance(products, dict):
            products = list(products.values())

        # Make sure we have a list
        if not isinstance(products, list):
            continue

        # Add to all products
        all_products.extend(products)

        # IMPORTANT:
        # create a NEW list for this file
        category_items.append(products.copy())

        # Get unique category names
        for product in products:
            category = product.get("category")

            if category and category not in categories:
                categories.append(category)

    return all_products, categories, category_items

# All Products Path
products_file = 'products.json'

# Create combained products item in one file
def create_products():
    """
    Create products.json containing all products.
    """
    with open("products.json", 'w') as file:
        json.dump(all_products, file, indent=4)
    return products


# Process 1
def find_category_and_product(user_input,products_and_category):
    delimiter = "####"
    system_message = f"""
    You will be provided with customer service queries. \
    The customer service query will be delimited with {delimiter} characters.
    Output a python list of json objects, where each object has the following format:
        'category': <one of Computers and Laptops, Smartphones and Accessories, Televisions and Home Theater Systems, \
    Gaming Consoles and Accessories, Audio Equipment, Cameras and Camcorders>,
    OR
        'products': <a list of products that must be found in the allowed products below>

    Where the categories and products must be found in the customer service query.
    If a product is mentioned, it must be associated with the correct category in the allowed products list below.
    If no products or categories are found, output an empty list.

    The allowed products are provided in JSON format.
    The keys of each item represent the category.
    The values of each item is a list of products that are within that category.
    Allowed products: {products_and_category}
    
    """
    messages =  [  
    {'role':'system', 'content': system_message},    
    {'role':'user', 'content': f"{delimiter}{user_input}{delimiter}"},  
    ] 
    return get_completion_from_messages(messages)


### Process 2
def get_products_and_category():
    """
    Get products grouped by category.
    """

    all_products, categories, category_items = get_products()

    products_by_category = defaultdict(list)

    for category, products in zip(categories, category_items):

        for product in products:

            if isinstance(product, dict):
                product_name = product.get("name")

                if product_name:
                    products_by_category[category].append(product_name)

    return dict(products_by_category)

### Process 3
def read_string_to_list(input_string):
    if input_string is None:
        return None

    try:
        input_string = input_string.replace("'", "\"")  # Replace single quotes with double quotes for valid JSON
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None

# Process 4
def generate_output_string(data_list):
    if not data_list:
        return ""
    products = get_mentioned_product_info(data_list)
    output_string = ""
    for product in products:
        output_string += json.dumps(product, indent=4) + "\n"
    return output_string
    
# Process 4
def get_mentioned_product_info(data_list):
    """
    Used in L5 and L6
    """
    product_info_l = []
    if not data_list:
        return product_info_l
    for data in data_list:
        try:
            # Product names were mentioned
            if "products" in data:
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        product_info_l.append(product)
                    else:
                        print(
                            f"Error: Product '{product_name}' not found"
                        )
            # Category was mentioned
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(
                    category_name
                )
                if category_products:
                    product_info_l.extend(category_products)
                else:
                    print(
                        f"Error: Category '{category_name}' not found"
                    )
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")
    return product_info_l


# Chat allowed category and items
def create_allowed_products_text(categories, category_items):
    sections = []
    for index, category in enumerate(categories):
        products = category_items[index]
        product_names = []
        for product in products:
            if isinstance(product, dict):
                product_names.append(product["name"])
            else:
                product_names.append(product)
        product_text = "\n".join(product_names)
        section = f"""{category} category:
{product_text}"""
        sections.append(section)
    return "\n\n".join(sections)

# Get Created product list
# def get_product_list():
#     """
#     Used in L4 to get a flat list of products
#     """
#     with open(products_file, 'r') as file:
#         products = json.load(file)
#     return products



# Need to check we need this fucntion or not
def get_product_by_name(name):

    all_products, categories, category_items = get_products()
    for product in all_products:
        if product.get("name") == name:

            return product

    return None


# Need to check we need this fucntion or not
def get_products_by_category(category):
    products = get_products()
    return [product for product in products.values() if product["category"] == category]

