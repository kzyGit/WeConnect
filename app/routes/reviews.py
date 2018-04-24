from flask import request, make_response, jsonify
from . import bs
from .. models import Business
from .. models import Review

@bs.route('/api/v1/businesses/<int:businessid>/review', methods=['POST'])
def create_a_business_review(businessid):
    """Endpoint to create a review for a given business"""
    title = str(request.data.get('title'))
    content = str(request.data.get('content'))
    
    if title and content:
        review = Review(title, content)
        for business in Business.business_list:
            if business.businessid == businessid:
                
                business.reviews.append(review)
                response =make_response(
                jsonify({
                    'message':'Review added successfully'
                    
                    }), 201)
                return response
                       
            else:
                response = make_response(
                jsonify({
                    'message':'No business with the given id'
                    
                    }), 404)
                return response

    else:
        response = make_response(jsonify({
                'message': "Incomplete Information"
                }
        ), 400)
        return response 


@bs.route('/api/v1/businesses/<int:businessid>/review', methods=['GET'])
def get_all_business_reviews(businessid):
    """Endpoint to retrieve all reviews for a business"""
  
    for business in Business.business_list:
        if business.businessid == businessid:
            if len(business.reviews) == 0:
                response = make_response(jsonify({
                    'message': "No reviews found"
                    }
                ), 404)
                return response

            for reviews in business.reviews:
                business_reviews = []
                business_review = {}
                business_review[reviews.title]= reviews.content
                business_reviews.append(business_review)
            response = make_response(jsonify({
                'Business reviews':business_reviews
                }
                ), 302)
            return response

        else:
             response =make_response(
                jsonify({
                    'message':'No business with the id'
                    
                    }), 404)
        return response    
       

    response = make_response(
            jsonify({
            'message':'No businesses found'
            
            }), 404)
            
    return response
