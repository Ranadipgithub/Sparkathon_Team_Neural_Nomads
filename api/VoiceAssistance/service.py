import random
from VoiceAssistance.utils import PredefinedResponseManager
# from app.db_repository import find_products , add_to_cart ,remove_from_cart
from VoiceAssistance.llm_engine import llm_output
from flask import session 

class IntentService:
    def __init__(self, intent_repository):
        self.intent_repository = intent_repository
        self.predefined_response_manager = PredefinedResponseManager()
        
    def order_service(self):
        try:
            if 'active_intent' not in session:
                if len(self.intent_repository['products']) == 0:
                    return random.choice(self.predefined_response_manager.product_not_found())

                products = find_products()
                if len(products) == 0:
                    return "Sorry, no products are available at the moment."

                available_products = []
                not_available_products = []

                for user_product in self.intent_repository['products']:
                    user_name = user_product['product'].strip().lower().replace(" ", "")
                    user_quantity = user_product['quantity']
                    found = False

                    for p in products:
                        db_name = p['productName'].strip().lower().replace(" ", "")
                        if db_name == user_name:
                            if p['quantity'] >= user_quantity:
                                available_products.append({
                                    "product": p['productName'],
                                    "quantity": user_quantity,
                                    "id": str(p['_id'])
                                })
                                found = True
                            else:
                                not_available_products.append(p['productName'])
                            break  # found or not, break once matched

                    if not found:
                        not_available_products.append(user_product['product'])

                if len(available_products) == 0:
                    return random.choice(self.predefined_response_manager.product_not_available())

                if len(not_available_products) > 0:
                    return f"Sorry, {', '.join(not_available_products)} are not available in the requested quantity."

                session['active_intent'] = {'intent': 'add_cart', 'products': available_products}
                return random.choice(self.predefined_response_manager.product_added_to_cart_query())

            else:
                print("This is the intent repository:", session['active_intent'])
                existing_cart = session['active_intent']
                print("This is the session:", existing_cart)

                if len(self.intent_repository['products']) != 0:
                    products = find_products()
                    if len(products) == 0:
                        return "Sorry, no products are available at the moment."

                    new_available = []
                    not_available_products = []

                    for user_product in self.intent_repository['products']:
                        user_name = user_product['product'].strip().lower().replace(" ", "")
                        user_quantity = user_product['quantity']
                        found = False

                        for p in products:
                            db_name = p['productName'].strip().lower().replace(" ", "")
                            if db_name == user_name:
                                if p['quantity'] >= user_quantity:
                                    new_available.append({
                                        "product": p['productName'],
                                        "quantity": user_quantity,
                                        "id": str(p['_id'])
                                    })
                                    found = True
                                else:
                                    not_available_products.append(p['productName'])
                                break

                        if not found:
                            not_available_products.append(user_product['product'])

                    if len(new_available) == 0:
                        return random.choice(self.predefined_response_manager.product_not_available())

                    if len(not_available_products) > 0:
                        return f"Sorry, {', '.join(not_available_products)} are not available in the requested quantity."

                    merged_cart = existing_cart['products'] + new_available
                    session['active_intent'] = {'intent': 'add_cart', 'products': merged_cart}
                    return random.choice(self.predefined_response_manager.product_added_to_cart_query())

                else:
                    # print("This is the session:----->>", session['active_intent']['products'])

                    user_cart = add_to_cart(session['active_intent']['products'])

                    if not user_cart:
                        return "Failed to add products to the cart. Please try again later."

                    if user_cart.get('status', False):
                        message = user_cart['message']
                    else:
                        message = "Failed to add products to the cart. Please try again later."

                    session.pop('active_intent', None)
                    return random.choice(self.predefined_response_manager.product_added_cart())

        except Exception as e:
            return f"An error occurred in order_service: {str(e)}"
        
    def login_service(self):
        try:
            predefined_response_manager= PredefinedResponseManager()
            response = predefined_response_manager.login_query()
            return random.choice(response)  
        except Exception as e:

            return   f"An error occurred in login_service: {str(e)}"

        
        
    def new_user_service(self):
        try:
            predefined_response_manager= PredefinedResponseManager()
            
            response = predefined_response_manager.new_user()
            
            return random.choice(response)  
        
        except Exception as e:

            return   f"An error occurred in login_service: {str(e)}"    
        
        
    
    def send_menu_service(self):
        try:
            predefined_response_manager= PredefinedResponseManager()
            
            response =predefined_response_manager.show_menu()
            
            return random.choice(response)  
        
        except Exception as e:

            return   f"An error occurred in login_service: {str(e)}"        
        
        
       
    def home_page_service(self):
        try:
            predefined_response_manager= PredefinedResponseManager()
            
            response = predefined_response_manager.show_home_page()
            
            return random.choice(response)  
        
        except Exception as e:

            return   f"An error occurred in login_service: {str(e)}"            
        
        
               
    def payment_service(self):
        try:
            predefined_response_manager= PredefinedResponseManager()
            
            response = predefined_response_manager.payment_page()
            
            return random.choice(response)  
        
        except Exception as e:

            return   f"An error occurred in login_service: {str(e)}"         
        
               
    def other_service(self):
        try:
            
            prompt = (
                        "You are a friendly voice assistant for a food ordering website. "
                        "The user has asked a general question not related to food items or cart actions. "
                        "Reply in **a single friendly and helpful sentence**, keeping your tone casual and clear."
                    )            
            response = llm_output(system_prompt=prompt)
            
            return response  
        
        except Exception as e:

            return   f"An error occurred in login_service: {str(e)}"       
  
            
    def product_query(self):
        try:
            products = find_products()

            if len(products) == 0:
                return "Sorry, no products are available at the moment."

            available_products = []
            not_available_products = []

            for requested in self.intent_repository['products']:
                product_name = requested['product'].lower().strip().replace(" ", "")
                product_quantity = requested['quantity']
                found = False

                for p in products:
                    if p['productName'].lower().strip().replace(" ", "") == product_name:
                        available_products.append({
                            "product": p['productName'],
                            "quantity": product_quantity,
                            "id": str(p['_id'])
                        })
                        found = True
                        break  # found match, no need to continue searching

                if not found:
                    not_available_products.append(product_name)


            if len(available_products) == 0:
                return random.choice(self.predefined_response_manager.product_not_available())

            if len(not_available_products) > 0:
                available = ", ".join([p['product'].capitalize() for p in available_products])
                not_available = ", ".join([name.capitalize() for name in not_available_products])
                return (
                    f"I found some of the items. {available} are available, "
                    f"but I'm sorry, {not_available} are currently out of stock."
                )

            return random.choice(self.predefined_response_manager.product_available())

        except Exception as e:
            return f"An error occurred in product_query: {str(e)}"
  
            
    def price_query(self):
        try:
            products = find_products()

            if len(products) == 0:
                return "Sorry, no products are available at the moment."

            price_responses = []
            not_found_items = []

            for product in self.intent_repository['products']:
                user_product_name = product['product'].strip().lower().replace(" ", "")
                found = False

                for p in products:
                    db_product_name = p['productName'].strip().lower().replace(" ", "")
                    if db_product_name == user_product_name:
                        price_responses.append(f"The price of {p['productName']} is ₹{p['price']}.")
                        found = True
                        break
                
                if not found:
                    not_found_items.append(product['product'])

            # Construct the response
            if not price_responses:
                return "Sorry, I couldn't find the prices for the items you mentioned."

            if not_found_items:
                not_found_text = ", ".join(not_found_items)
                return (
                    f"{' '.join(price_responses)} However, I couldn't find the price for {not_found_text}."
                )

            return " ".join(price_responses)

        except Exception as e:
            return f"An error occurred in price_query: {str(e)}"
            
            
    def product_description_query(self):
        try:
            products = find_products()

            if len(products) == 0:
                return "Sorry, no products are available at the moment."

            description_responses = []
            not_found_items = []

            for product in self.intent_repository['products']:
                user_product_name = product['product'].strip().lower().replace(" ", "")
                found = False

                for p in products:
                    db_product_name = p['productName'].strip().lower().replace(" ", "")
                    if db_product_name == user_product_name:
                        description_responses.append(
                            f"{p['productName']}: {p['description']}"
                        )
                        found = True
                        break

                if not found:
                    not_found_items.append(product['product'])
            
            print("This is the description responses:",description_responses)
            print("This is the not found items:",not_found_items)        

            if not description_responses:
                return "Sorry, I couldn't find descriptions for the items you mentioned."

            if not_found_items:
                not_found_text = ", ".join(not_found_items)
                return (
                    f"{' '.join(description_responses)} However, I couldn't find descriptions for {not_found_text}."
                )

            return " ".join(description_responses)

        except Exception as e:
            return f"An error occurred in product_description_query: {str(e)}"
    
        
    def remove_from_cart_query(self):
        try:
            # Get the active session's cart
            active_session = session.get('active_intent', None)

            product_list = self.intent_repository['products']
            print("This is the response from remove_from_cart:",product_list)
            if active_session is None:
                # If no session exists, call backend cart service
                response = remove_from_cart(product_list)
                

                if not response:
                    return "Failed to remove products from the cart. Please try again later."
                if response.get('status', False):
                    return f"{response['message']} has been removed from your cart."
                else:
                    return "Product could not be removed from your cart."

            else:
                # Remove items from session cart manually
                removed_items = []
                updated_items = []
                not_found_items = []

                for target in product_list:
                    target_name = target['product'].strip().lower().replace(" ", "")
                    target_quantity = target.get('quantity', 1)
                    found = False

                    for item in active_session.get('products', []):
                        item_name = item['product'].strip().lower().replace(" ", "")
                        if item_name == target_name:
                            found = True
                            if item['quantity'] > target_quantity:
                                item['quantity'] -= target_quantity
                                updated_items.append(f"{item['product']} (reduced by {target_quantity})")
                            else:
                                active_session['products'].remove(item)
                                removed_items.append(item['product'])
                            break

                    if not found:
                        not_found_items.append(target['product'])

                # Construct response
                response_parts = []

                if updated_items:
                    response_parts.append(f"Updated quantities: {', '.join(updated_items)}.")

                if removed_items:
                    response_parts.append(f"Removed from cart: {', '.join(removed_items)}.")

                if not_found_items:
                    response_parts.append(f"Couldn't find: {', '.join(not_found_items)} in your cart.")
                    
                if updated_items or removed_items: 
                       
                    session['active_intent'] = active_session
                    response = remove_from_cart(product_list)
                    return random.choice(self.predefined_response_manager.updated_cart())
                        

                if not response_parts:
                    return "None of the items you mentioned were found in your cart."

                return " ".join(response_parts)
        except Exception as e:
            return f"An error occurred in remove_from_cart_query: {str(e)}"
  
  
    
    def watch_cart_service(self):
        try:
            predefined_response_manager= PredefinedResponseManager()
            
            response =predefined_response_manager.watch_cart()
            
            return random.choice(response)  
        
        except Exception as e:

            return   f"An error occurred in login_service: {str(e)}"        
                   