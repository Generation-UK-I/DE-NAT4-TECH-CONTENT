# A Cat-as-a-Service App

In this busy, connected, always online world, we're busier and more stressed than ever. What can we do to resolve this crisis?

You could get a cat! But that's even more hassle, and who wants that judgemental face staring at them all day. Let alone the 'presents' they leave on the door mat.

What if you could have all of the benefits, and none of the responsibilities? There is clearly a gap in the market!

Introducing Cat as a Service - Just like SaaS revolutionised software access and licensing, CaaS aims to do the same for your feline needs.

---

You will initially build a simple request/response app to deliver a cat on demand.

- Create a new working directory and open it in VSC.
- Install the **requests** and **pillows** libraries: `pip install requests pillow`
  - `requests`: Send HTTP requests, and handle responses
  - `pillows`: Python Image Library (PIL)
- Create a new Python file and add the following code.

```py
import requests
from PIL import Image
from io import BytesIO
 
# 1. Define the API endpoint
url = "https://cataas.com/cat"
 
# 2. Make a GET request to the API
response = requests.get(url)
 
# 3. Check the request was successful
print(f"Status code: {response.status_code}")
 
# 4. Load the image from the response and display it
image = Image.open(BytesIO(response.content))
image.show()
```

### Code breakdown

- `import...`: Import `requests`, `Image` (from pillows), and `BytesIO` (from io)
  - `Image`: Part of PIL, provides various functions, including loading and creating images.
  - `io`: Part of the Python Standard Library, it is the main way of dealing with various types of I/O (input/output), including text, binary, and RAW.
    - `BytesIO`: We've spent a lot of time working with strings, but other file types comprising binary data, like images, work differently. These are split into bytes, and `ByteIO` allows us to work with these bytes.
- `url = "https://cataas.com/cat"`:This is the API endpoint, i.e. a specific address on a server that represents every piece of data or functionality an API exposes. `/cat` tells the server to return a random cat image"
- `response = requests.get(url)`: This is where the actual API call happens. `requests.get()` sends an HTTP GET request to the server — The server receives it, and returns a random cat image. Everything the server sends back is stored in the `response` object.
- `print(f"Status code: {response.status_code}")`: Every API response includes a status code — a 3-digit number that tells you whether the request succeeded or failed.

    The most important status code categories are:

    - 200 = Success
    - 4XX = Client errors (e.g. 404: not found - you requested a resource which doesn't exist).
    - 5XX = Server errors (e.g. 503: Requested service is unavailable)

- `image = Image.open(BytesIO(response.content))`: The `response.content` attribute holds the raw bytes the server sent back — in this case, the image file itself. `BytesIO` wraps those bytes in a file-like object so that PIL can read them without saving to disk first.
- `image.show()`: Opens the image in your system's default viewer.

>Some APIs return JSON (text data), others return binary data like images, PDFs, or audio. You handle them differently — JSON uses `response.json()`, binary uses `response.content`.

---

Our app works, but there is more functionality available at the CaaS API.

### Path vs Query Parameters

When making API calls, parameters are how you send extra information to the server. The two main types are **path** parameters and **query** parameters - and they appear in different parts of the URL.

- **Path** parameters identify what you want.
- **Query** parameters specify how you want it.

#### Path Parameters

Path path parameters are part of the URL itself, and they identify the resource you want. The path may be multiple layers deep, depending upon how the resources are organised on the server.

```text
http://cataas.com/cat/orange/cat_472   # Not a real endpoint
                 |---path-param----|
|-------------URL------------------|
```

The path parameter points to the location of a specific resource, in this case `cat_472`. Other examples of path parameters could be:

```text
/products/123
/orders/2024/55
/blog/posts/hello-world
```

#### Query Parameters

After the path parameters you can add a `?` then provide query parameters which describe how you want the response to be returned.

Some commonly used parameters include:

- Filtering (`?status=active`)
- Sorting (`?sort=price`)
- Pagination (`?page=2&limit=20`)
- Optional settings (`?include=photos`)

In context they might look like this:

```text
/products?category=books&price_lt=20
/search?q=aws+training
```

>NOTICE: The query parameters are simply key:value pairs - which we've used many times.

Query parameters are usually optional, the request will work without them, but with default options.

### Improving our App

We're going to build out functionality by adding one path parameter, and one query parameter to our app.

The two parameters we're going to implement are:

- Path: The API we're using allows us to overlay a text string on the returned cat image, this is achieved by appending `/says/[string]` to the base URL.
- Query: The API also allows us to select the size of the cat image returned, from the options `xsmall`, `small`, `medium`, or `square`, this is done by appending `?type=medium` to the base URL.

#### Adding the path parameter

Here's the code, we import the same libraries used previously, and the code is now in functions for improved useability, testing, modularity, easier development, and so on.

```py
def build_path_parameter():
    say_text = input("What should your cat say?\n(ENTER for nothing)\n>")
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
```

**Breakdown**:

1. First we store the user input for the overlaid text
2. If some input is provided the full path parameter is built, if not the base_url is unchanged.
3. Create a response object, which calls the url using the `requests.get()` method and any input from the user is passed through. `requests` will add `%20` to handle spaces correctly if necessary.
4. Once the response is received, print the response code and full URL requested by calling the `.status_code` and `.url` attributes
5. The last two lines are the same as we used previously to load and display the image.

#### Adding the query parameter

Handling the query parameter isn't too different to the path, we just need to build the endpoint URL correctly, but using slightly different data types. As you saw in earlier examples, query parameters are typically key value pairs, which in Python means dictionaries.

```py
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
```

**Breakdown**:

1. As with the path parameter, we capture user input, in this case prompting with options (*missing input validation - you should fix*)
2. Declare an empty dictionary for the chosen parameters
3. The only key value pair we're using in this case is `type`, but APIs can support multiple.

  Add the parameter to the dictionary by adding the key `type` and whatever input was provided as the value.
4. The response object again uses the `requests.get()` method with both the `base_url` and the `params` passed through. `requests` automatically handles formatting the url correctly, including adding the `?` before the parameters.
5. As with the path function, the status code and url are printed, then the response content is loaded and displayed.

Here's the final code, including a simple menu to allow the user to select the functions.

```py
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
    say_text = input("What should your cat say?\n(ENTER for nothing)\n>")
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
    
while True:
    prompt = "Welcome to the Cat as a Service App\n"
    prompt += "Please select your furball\n"
    prompt += "Main menu:\n"
    prompt += "1. Deliver a cat of a selected size\n"
    prompt += "2. Deliver a cat which speaks\n"
    prompt += "0. Quit"
    print(prompt)
    main_choice = input("Selection:\n>")
    if main_choice == "1":
        all_params = build_query_parameters()
    elif main_choice == "2":
        path_url = build_path_parameter()
    elif main_choice == "0":
        break
    else:
        print("Please make a valid selection.")
```

There is a lot of additional functionality available at the cat-as-a-service API. After finishing this tutorial you should review them on the [website here](https://cataas.com), and experiment with adding further functionality.
