from VoiceAssistance.utils import PromptManager
from VoiceAssistance.llm_engine import llm_output
from VoiceAssistance import voiceBlueprint
from VoiceAssistance.service import IntentService
from VoiceAssistance.utils import PredefinedResponseManager, speak
import json
from flask import request, jsonify
from flask import session
import random


@voiceBlueprint.route('/', methods=['POST'])
def voiceAssistanceInput():
    try:
        input_data = request.form['text']
        if( not input_data):
            return jsonify({'error': 'No input data provided'}), 400
        if len(input_data) > 1000:
            return jsonify({'error': 'Input data exceeds maximum length of 1000 characters'}), 400
        # Create a PromptManager instance
        
        prompt_manager = PromptManager(input_data)
        
        system_prompt = prompt_manager.intentPrompt()
        
        response = llm_output(system_prompt=system_prompt)
        
        if not response:
            return jsonify({'error': 'No response from the model'}), 500
        # Return the response as JSON
        
        try:
            response = json.loads(response)
        except json.JSONDecodeError as e:
            return jsonify({'error': f'LLM response is not valid JSON: {str(e)}', 'raw_response': response}), 500
        
        if not isinstance(response, dict):
            return jsonify({'error': 'Invalid response format from the model'}), 500
        
        active_intent = session.get('active_intent', None) 
        
        
        if( response['intent'] == 'confirm_intent' and active_intent is None):
            try:
                
                response =  random.choice([
                "Hmm, there's nothing to confirm right now. Would you like to place an order or see the menu?",
                "I'm not sure what you're confirming — let me know what you want to do next.",
                "There's no current action to proceed with. Want to browse the menu or check your cart?",
                "You said yes, but I don't have any action to confirm. Try telling me what you'd like to do!",         
                ])
        
                speak(response)

                return jsonify({
                    'message': 'No active intent to confirm.',
                    'response':response,
                    'intent': 'confirm_intent'
                }), 200
            except Exception as e:
                return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500
                
               
        if ( response['intent'] == 'cancel_intent'):
            try:
                session.pop('active_intent', None)

                response = random.choice([
                    "Okay, I have cancelled that for you.",
                    "Sure, I have cancelled.",
                    "No problem, I have cancelled that.",
                    "Alright, I have cancelled that for you.",
                    "Got it, I have cancelled that for you.",
                ])
                speak(response)
            
                return jsonify({
                    'message': 'Intent cancelled successfully.',
                    'response': response ,
                    'intent': 'cancel_intent'
                }), 200
            except Exception as e:
                return jsonify({'error': f'An unexpected error occurred: {str(e)}'}),
 
        
        if(response['intent'] == 'add_cart'  or (response['intent'] == 'confirm_intent' and active_intent['intent']!=None and active_intent['intent'] == 'add_cart')):
            
            order_intent = IntentService(response)
        
            response_data = order_intent.order_service()
            
            speak(response_data)
            
            if not response_data:
                return jsonify({'error': 'Failed to process order service'}), 500
            
            return jsonify({
                'message': 'Successfully processed order service.',
                'response': response_data,
                'intent': 'add_cart'
            }), 200
            
            
        if(response['intent'] == 'log_in'):
            
            login_intent = IntentService(response)
        
            response_data = login_intent.login_service()
            speak(response_data)
            
            if not response_data:
                return jsonify({'error': 'Failed to process order service'}), 500
            
            return jsonify({
                'message': 'Successfully processed order service.',
                'response': response_data,
                'intent': 'log_in'
            }), 200
            
            
        if(response['intent'] == 'new_user'):
            
            newuser_intent = IntentService(response)
        
            response_data = newuser_intent.new_user_service()
            
            speak(response_data)
            if not response_data:
                return jsonify({'error': 'Failed to process order service'}), 500
            
            return jsonify({
                'message': 'Successfully processed order service.',
                'response': response_data,
                'intent': 'new_user'
            }), 200
            
                           
        if(response['intent'] == 'send_menu'):
            
            sendmenu_intent = IntentService(response)
        
            response_data = sendmenu_intent.send_menu_service()
            speak(response_data)
            
            if not response_data:
                return jsonify({'error': 'Failed to process order service'}), 500
            
            return jsonify({
                'message': 'Successfully processed order service.',
                'response': response_data,
                'intent': 'send_menu'
            }), 200
            
            
        if(response['intent'] == 'home_page'):
            
            homepage_intent = IntentService(response)
        
            response_data = homepage_intent.home_page_service()
            
            speak(response_data)
            if not response_data:
                return jsonify({'error': 'Failed to process order service'}), 500
            
            return jsonify({
                'message': 'Successfully processed order service.',
                'response': response_data,
                'intent': 'home_page'
            }), 200
            
            
        if(response['intent'] == 'payment'):
            
            payment_intent = IntentService(response)
        
            response_data = payment_intent.payment_service()
            
            speak(response_data)
            if not response_data:
                return jsonify({'error': 'Failed to process order service'}), 500
            
            return jsonify({
                'message': 'Successfully processed order service.',
                'response': response_data,
                'intent': 'payment'
            }), 200
 
            
        if(response['intent'] == 'other_queries'):
            
            payment_intent = IntentService(response)
        
            response_data = payment_intent.other_service()
            
            speak(response_data)
            if not response_data:
                return jsonify({'error': 'Failed to process order service'}), 500
            
            return jsonify({
                'message': 'Successfully processed order service.',
                'response': response_data,
                'intent': 'other_queries'
            }), 200
            
            
        if(response['intent'] == 'search_in_product'):
            
            product_query_intent = IntentService(response)
        
            response_data = product_query_intent.product_query()
            speak(response_data)
            
            if not response_data:
                return jsonify({'error': 'Failed to process order service'}), 500
            
            return jsonify({
                'message': 'Successfully processed order service.',
                'response': response_data,
                'intent': 'search_in_product'
            }), 200
            
            
        if(response['intent'] == 'price_intent'):
            
            price_intent = IntentService(response)
        
            response_data = price_intent.price_query()
            speak(response_data)
            
            if not response_data:
                return jsonify({'error': 'Failed to process order service'}), 500
            
            return jsonify({
                'message': 'Successfully processed order service.',
                'response': response_data,
                'intent': 'price_intent'
            }), 200
            

        if(response['intent'] == 'product_query'):
            
            product_description_intent = IntentService(response)
        
            response_data = product_description_intent.product_description_query()
            
            speak(response_data)
            if not response_data:
                return jsonify({'error': 'Failed to process order service'}), 500
            
            return jsonify({
                'message': 'Successfully processed order service.',
                'response': response_data,
                'intent': 'product_query'
            }), 200
            

        if(response['intent'] == 'remove_from_cart'):
            
            remove_cart_intent = IntentService(response)
        
            response_data = remove_cart_intent.remove_from_cart_query()
            speak(response_data)
            if not response_data:
                return jsonify({'error': 'Failed to process order service'}), 500
            
            return jsonify({
                'message': 'Successfully processed order service.',
                'response': response_data,
                'intent': 'remove_from_cart'
            }), 200


        if(response['intent'] == 'watch_cart'):
            
            watchcart_intent = IntentService(response)
        
            response_data = watchcart_intent.watch_cart_service()
            
            speak(response_data)
            if not response_data:
                return jsonify({'error': 'Failed to process order service'}), 500
            
            return jsonify({
                'message': 'Successfully processed order service.',
                'response': response_data,
                'intent': 'watch_cart'
            }), 200


        return jsonify({
            'message': 'Successfully got the response.',
            'response': response,
            'intent' : response['intent']
        }), 200        
            
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500



@voiceBlueprint.route('/welcome', methods=['POST'])
def welcome():
    try:
        response = request.form.get('user_info', None)
        print("This is the response from the welcome route:", response)
        session['user_info']=response    
        predefined_response_manager = PredefinedResponseManager()
        response = predefined_response_manager.welcome_messeges()
        response = random.choice(response)
        
        speak(response)
                
        return jsonify({
            'message': 'Welcome message sent successfully.',
            'response': response,
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500
    
    


@voiceBlueprint.route('/clear', methods=['POST'])
def clear():
    try:
        session.pop('user_info',None)  
        session.pop('active_intent',None)
        return jsonify({
            'message': 'Welcome message sent successfully.',
            'response': "Successfully removed the session!!",
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500
    
    