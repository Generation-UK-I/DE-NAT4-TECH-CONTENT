import requests
from PIL import Image
from io import BytesIO


image_type = ""
base_url = "https://cataas.com/cat"

def build_query_parameters():
    image_type = input("What size should your cat be?\n(xsmall, small, medium or square (BLANK for random))\n>")
    params = {}
    if image_type:
        params["type"] = image_type
        
    response = requests.get(base_url, params)

    print(f"Status code: {response.status_code}")
    print(f"Full URL requested: {response.url}")
    # STEP 4: Display the image
    image = Image.open(BytesIO(response.content))
    image.show()

def build_path_parameter():
    say_text = input("What should your cat say? (ENTER for nothing)\n>")
    if say_text:
        url = f"{base_url}/says/{say_text}"
    else:
        url = base_url
    response = requests.get(url)
    print(f"Status code: {response.status_code}")
    print(f"Full URL requested: {response.url}")
    # STEP 4: Display the image
    image = Image.open(BytesIO(response.content))
    image.show()

# def make_get_request(url, user_params):
#     response = requests.get(url, params=user_params)

#     print(f"Status code: {response.status_code}")
#     print(f"Full URL requested: {response.url}")
#     # STEP 4: Display the image
#     image = Image.open(BytesIO(response.content))
#     image.show()
    
while True:
    prompt = "Welcome to the Cat as a Service App\n"
    prompt += "Please select your furball\n"
    prompt += "Main menu:\n"
    prompt += "1. Deliver a cat of a selected size\n"
    prompt += "2. Deliver a cat which speaks\n"
#    prompt += "3. Deliver a default cat\n"
    prompt += "0. Quit"
    print(prompt)
    main_choice = input("Selection:\n>")
    if main_choice == "1":
        all_params = build_query_parameters()
    elif main_choice == "2":
        path_url = build_path_parameter()
    elif main_choice == "3":
        make_get_request(path_url, all_params)
    elif main_choice == "0":
        break
    else:
        print("Please make a valid selection.")
