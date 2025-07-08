import pyttsx3




class PromptManager():
    def __init__(self, user_prompt):
        self.user_prompt = user_prompt
        
    def intentPrompt(self) -> str:
        system_prompt = '''
    You are a smart voice assistant for a food ordering app. Your task is to return only a valid **raw JSON object** — no explanations, no markdown, no backticks.

    ### Your Goals:
    1. Identify the user's **intent** from their message.
    2. Extract **food item names and quantities**, only if applicable.

    ### Supported Intents:
    - confirm_intent: user confirms a previous intent or action (e.g., "Yes", "Sure", "That's right", "Please proceed" , "Go ahead" , "Ok")
    - cancel_intent: user cancels or denies a previous intent (e.g., "No", "Nevermind", "I changed my mind", "Forget it")
    - log_in: user wants to log in (e.g., "Sign in", "Log me in")
    - new_user: user wants to create a new account (e.g., "Register me", "I need an account")
    - send_menu: user wants to view the menu or categories (e.g., "What food do you have?")
    - home_page: user wants to return to the home page (e.g., "Take me home")
    - add_cart: user wants to order/add food (e.g., "I want a burger", "Add fries")
    - remove_from_cart: user wants to remove items (e.g., "Remove coke")
    - search_in_product: user wants to search or explore food (e.g., "Do you have biryani?")
    - product_query: user asks about food properties (e.g., "Is it spicy?")
    - price_intent: user asks about cost (e.g., "How much is the burger?")
    - payment: user wants to pay or checkout
    - watch_cart: user wants to see their cart
    - other_queries: general questions not covered by the above

    ### Output Rules:
    - Return a raw JSON object, nothing else.
    - For intents not involving food items, `products` should be an empty list.
    - For `add_cart` or `remove_from_cart`, extract `product` and `quantity` (default to 1 if not specified).
    - For `search_in_product`, `product_query`, `price_intent`: extract `product`, use `quantity: null`.

    ### Output Format:
    {{
    "intent": "<intent_label>",
    "products": [
        {{"product": "<item_name>", "quantity": <number or null>}}
    ]
    }}

    ### Examples:

    User: "I want to order 2 cheeseburgers and a coke"  
    Output:
    {{
    "intent": "add_cart",
    "products": [
        {{"product": "cheeseburgers", "quantity": 2}},
        {{"product": "coke", "quantity": 1}}
    ]
    }}

    User: "Show me the cart"  
    Output:
    {{
    "intent": "watch_cart",
    "products": []
    }}

    User: "Remove the coke from my order"  
    Output:
    {{
    "intent": "remove_from_cart",
    "products": [
        {{"product": "coke", "quantity": 1}}
    ]
    }}

    User: "Is the biryani spicy?"  
    Output:
    {{
    "intent": "product_query",
    "products": [
        {{"product": "biryani", "quantity": null}}
    ]
    }}

    User: "Do you have five biryani?"  
    Output:
    {{
    "intent": "product_query",
    "products": [
        {{"product": "biryani", "quantity": 5}}
    ]
    }}

    User: "How much is the paneer pizza?"  
    Output:
    {{
    "intent": "price_intent",
    "products": [
        {{"product": "paneer pizza", "quantity": null}}
    ]
    }}

    User: "Show me the menu"  
    Output:
    {{
    "intent": "send_menu",
    "products": []
    }}

    User: "Log me in please"  
    Output:
    {{
    "intent": "log_in",
    "products": []
    }}

    User: "Yes, go ahead and order"  
    Output:
    {{
    "intent": "confirm_intent",
    "products": []
    }}

    User: "No, cancel the order"  
    Output:
    {{
    "intent": "cancel_intent",
    "products": []
    }}

    ### Now analyze the following user message:

    User: "{user_prompt}"

    Output:
    '''
        return system_prompt.format(user_prompt=self.user_prompt)
        
class PredefinedResponseManager():
    def __init__(self):
        pass

    def product_not_found(self):
        product_quantity_prompts = [
            "Please tell me the product name and the quantity you'd like to add to your cart.",
            "What product do you want to add? Please also mention how many units you need.",
            "Sure! Could you please provide the product name and how many you want?",
            "I can help you with that. Tell me the product and the quantity you'd like to order.",
            "Let me know what you want to buy and how many items you need.",
            "Please enter or say the product name followed by the quantity.",
            "Which product are you looking for, and how many units do you want?",
            "To proceed, I need the product name and quantity. For example, 'two ball pens'.",
            "Alright! Just give me the name of the product and how many you want.",
            "Before I add it to your cart, please mention both the item and the quantity."
        ]

        return product_quantity_prompts


    def product_added_cart(self):
        product_added_responses = [
            "The product has been successfully added to your cart.",
            "Got it! I've added the item to your cart.",
            "Item successfully added to your cart.",
            "Your product is now in the cart.",
            "Done! The product has been added.",
            "Successfully added the item to your cart.",
            "The item you requested is now in your cart.",
            "Product added. Let me know if you need anything else.",
            "It’s in your cart! You can continue shopping.",
            "Added to cart successfully. What would you like to do next?"
]


        return product_added_responses


    def product_not_available(self):
        product_not_available_responses = [
            "Sorry, this product is currently unavailable. Please check back later or explore similar options.",
            "Unfortunately, the item you're looking for is not in our inventory at the moment.",
            "We apologize, but this product is out of stock and cannot be added to your cart right now.",
            "This item has just sold out. We're working to restock it as soon as possible.",
            "Oops! That product is no longer available. You may want to browse alternative options.",
            "The product you requested is temporarily unavailable. Try again later or choose a different item.",
            "Looks like that item isn't available for purchase right now. Thank you for your patience!",
            "We're sorry! This product has been discontinued or is currently not offered.",
        ]
        
        return product_not_available_responses
    
    
    def product_added_to_cart_query(self):
        product_added_to_cart_query = [
            "Do you want to add the items to your cart?",
            "Would you like to proceed with adding these items to your cart?",
            "Shall I add these products to your cart?",
            "Do you want me to add these items to your shopping cart?",
            "Should I go ahead and add these products to your cart?",
            "Would you like to confirm adding these items to your cart?",
            "Do you want to proceed with adding these products to your cart?",
        ]
        return product_added_to_cart_query
    
    
    def login_query(self):
        
        LOGIN_RESPONSES = [
            "I’m redirecting you to the login page. Please log in here.",
            "Sure! Please log in to continue.",
            "Taking you to the login screen now.",
            "Redirecting... Kindly enter your login credentials.",
            "Let’s get you signed in. Please use the login page.",
            "You need to log in first. Sending you to the login page.",
            "Just a second, I’m opening the login page for you.",
            "Hold on! Redirecting you to your login portal.",
            "Please log in to access your account.",
            "Accessing login page. Kindly log in to proceed."
        ]

        return LOGIN_RESPONSES
    
     
    def new_user(self):
        
        NEW_USER_RESPONSES = [
            "Okay! I’m redirecting you to the new user registration page.",
            "Sure, let’s create your account. Taking you to the sign-up page now.",
            "Let’s get you started. Redirecting to the new user setup page.",
            "No problem! I’m sending you to the registration screen.",
            "Creating a new account? I’m taking you there now.",
            "Alright, heading over to the new user form. Please fill it in.",
            "I’ll help you register. Redirecting you to the new user page.",
            "Got it! You’ll be on the sign-up page in just a second.",
            "Starting fresh? I’m opening the new user registration now.",
            "Welcome! Let’s create your account. Redirecting..."
        ]
        return NEW_USER_RESPONSES            

    
    def show_menu(self):
        SEND_MENU_RESPONSES = [
            "I’m showing you the menus I have right now.",
            "Here’s what’s on the menu. Take a look!",
            "These are the categories available. Feel free to explore.",
            "Here’s the main menu with everything I can help you with.",
            "I’ve pulled up the menu for you — just pick a category.",
            "Check out these sections — it’s everything I’ve got!",
            "These are the options available. What would you like to explore?",
            "Take a look at the menu — you’ll find everything here.",
            "Here’s what I have in store for you.",
            "Showing you all available menus now."
]
        return SEND_MENU_RESPONSES        
    
            
    def show_home_page(self):
        
        HOME_PAGE_RESPONSES = [
            "I'm showing you the home page now.",
            "Taking you back to the home page.",
            "Here's the home page for you.",
            "Redirecting you to the home screen.",
            "Opening the home page right away.",
            "Showing you the main page now.",
            "Bringing up the home page.",
            "Here's your home page.",
            "Going back to the home page.",
            "Let me take you to the home screen."
        ]
        return HOME_PAGE_RESPONSES
    
                
    def payment_page(self):
        PAYMENT_RESPONSES = [
    "I'm redirecting you to the payment page.",
    "Taking you to checkout to complete your payment.",
    "Here's the payment page. Please proceed when ready.",
    "Opening the payment gateway for you.",
    "Let's get your payment processed. Redirecting now.",
    "Proceeding to payment. You can review your order here.",
    "Redirecting to the checkout page.",
    "You're all set to pay. Showing the payment options now.",
    "Ready to pay? I'm taking you to the payment screen.",
    "Opening payment section for you."
]
        return PAYMENT_RESPONSES


    def watch_cart(self):
        WATCH_CART_RESPONSES = [
            "Here's your cart. You can review your items.",
            "I'm showing you what's in your cart right now.",
            "Let's take a look at your shopping cart.",
            "Here's everything you've added to your cart.",
            "Your cart is ready. Check out the items inside.",
            "I've pulled up your cart for you.",
            "Here's what you have in your shopping cart.",
            "Let me show you the contents of your cart.",
            "This is your current shopping cart.",
            "You can see your cart items here."]
        return WATCH_CART_RESPONSES
    
    def product_available(self):
        PRODUCT_AVAILABLE_RESPONSES = [
            "Great! The product is available.",
            "Yes, we have that product in stock.",
            "Good news! The item you requested is available.",
            "The product is ready for you.",
            "Yes, we can add that to your cart.",
            "The item is available and can be added to your order.",
            "You can proceed with that product; it's in stock.",
            "The product is available for purchase.",
            "You can go ahead and add that item to your cart.",
            "That product is available and ready for you."]
        return PRODUCT_AVAILABLE_RESPONSES
    
    def updated_cart(self):
        UPDATED_CART_RESPONSES = [
            "Your cart has been updated successfully.Now ",
            "I've made the changes to your cart.",
            "Your cart is now up to date.",
            "The items in your cart have been modified.",
            "I've updated your cart with the latest changes.",
            "Your shopping cart has been refreshed.",
            "The cart has been adjusted as per your request.",
            "I've applied the updates to your cart.",
            "Your cart reflects the latest changes now.",
            "The modifications to your cart are complete."]
        return UPDATED_CART_RESPONSES
    
    def welcome_messeges(self):       
        welcome_responses = [
            "Welcome to Swad Desi! What would you like to eat today?",
            "Hi there! Craving something desi and delicious?",
            "Namaste! Swad Desi is ready to serve you something tasty!",
            "Welcome back to Swad Desi — your desi food journey starts here!",
            "Hello! Ready to explore the Swad Desi menu?",
            "Nice to see you again at Swad Desi! What's on your mind today?",
            "Hungry? Swad Desi has something mouth-watering waiting for you!",
            "Hey foodie! Let’s find something amazing to eat at Swad Desi!",
            "Welcome! Swad Desi is your assistant for all things delicious and desi.",
            "Let’s get started — biryani, chole bhature, or something sweet from Swad Desi?"
        ]
        return welcome_responses      
    
    
def speak(input_text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voices', voices[1].id)
    engine.say(input_text)
    engine.runAndWait()
        
           