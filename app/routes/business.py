from flask import request, make_response, jsonify
from . import bs
from .. models import Business

@bs.route('/')
@bs.route('/api/businesses', methods=['POST'])
def register_business():

    business_name = str(request.data.get('business_name'))
    about = str(request.data.get('about'))
    location = str(request.data.get('location'))
    contacts = str(request.data.get('contacts'))
          
    if business_name and about and location and contacts:
        for business in Business.business_list:
            if business.business_name == business_name:
                response =make_response(
                jsonify({
                    'message':'business already exists'
                    
                    }), 503)
                return response
        business = Business(business_name=business_name, about=about, location=location, contacts=contacts)
        business.save(business)
        response =make_response(
            jsonify({
                'message':'business added successfully'
                
                }), 201)
        return response
    else:
        response = make_response(jsonify({
                'message': "incomplete information"
                }
        ), 404)
        return response 

@bs.route('/api/businesses', methods=['GET'])
def retrieve_all_businesses():
        
    

        if len(Business.business_list) == 0:
            response = make_response(jsonify({
                'message': "No businesses found"
                }
            ), 404)
            return response

        else:
            businesses={}
            for business in Business.business_list:
                business.business_name
                business.businessid
                businesses.update({business.business_name:business.businessid})


            response = make_response(
                jsonify({
                'message':'Available Businesses',
                'businesses': businesses
                
                }), 200)
            
            return response

@bs.route('/api/businesses/<businessid>', methods=['GET'])
def get_businesses_by_id(businessid):
        Business.business_list
    

        if len(Business.business_list) == 0:
            response = make_response(jsonify({
                'message': "No businesses available"
                }
            ), 404)
            return response

        else:
            businesses={}
            for business in Business.business_list:
                if businessid == business.businessid:
                    business.business_name
                    business.businessid
                    businesses.update({business.businessid:business.business_name})


                    response = make_response(
                        jsonify({
                        'message':'Business found:',
                        'businesses': businesses
                        
                        }), 200)
                    
                    return response
                response = make_response(
                    jsonify({
                    'message':'Business not found:',
                    'businesses': businesses
                    
                    }), 404)
                    
                return response

@bs.route('/api/businesses/<businessid>', methods=['PUT'])
def update_businesses(businessid):
    business_name = str(request.data.get('business_name'))
    location = str(request.data.get('location'))
    contacts = str(request.data.get('contacts'))
    about = str(request.data.get('about'))

    for business in Business.business_list:
        if businessid == business.businessid:
            business.business_name=business_name
            business.location=location
            business.contacts=contacts
            business.about=about

        response = make_response(
                    jsonify({
                    'message':'Business Updated'
                    
                    }), 200)
                
        return response
    response = make_response(
                    jsonify({
                    'message':'Business not found'
                    
                    }), 404)
                
    return response

@bs.route('/api/businesses/<businessid>', methods=['DELETE'])
def delete_businesses(businessid):
    

    for business in Business.business_list:
        if businessid == business.businessid:
            Business.business_list.remove(business)

            response = make_response(
                        jsonify({
                        'message':'The business deleted successful'
                        
                        }), 204)
                    
            return response
    response = make_response(
        jsonify({
        'message':'The business not found'
        
        }), 404)
                
    return response