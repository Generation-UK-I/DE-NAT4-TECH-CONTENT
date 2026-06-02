import json
import os

def lambda_handler(event, context):
    """
    Lambda handler function that AWS Lambda uses as an entry point to Python code by default.
    
    Parameters:
        event (dict): The event payload containing request data
        context (LambdaContext): The runtime information of the Lambda invocation. The LambdaContext type is an internal AWS class that holds runtime metadata about the Lambda invocation e.g. request ID, function name, timeout
    
    Returns:
        dict: A JSON-formatted HTTP response with statusCode and body.
    """
    
    print(f'lambda_handler: event={event}, context={context}')
    movie = os.environ['FAVE_MOVIE']
    print(f'lambda_handler: movie={movie}')

    response_json = {
        'message': 'Hello Rory'
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(response_json) #converts Python object to JSON-formatted string
    }
