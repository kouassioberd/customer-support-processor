from typing import List, Dict

def load_test_data() -> List[Dict[str, str]]:
    """Load test support tickets covering all categories"""
    
    # Create sample test data covering all categories
    test_tickets = [
        {
            "category": "technical",
            "message": "hi my app keeps crashing when i try to open it pls help fix it thx"
        },
        {
            "category": "billing",
            "message": "i was charged twice for my subscription this month can u refund one of them"
        },
        {
            "category": "general",
            "message": "how do i change my password i cant find the settings option anywhere"
        },
        {
            "category": "complaint",
            "message": "this is the worst service ever i've been waiting for support for 3 hours and nobody is helping me"
        },
        {
            "category": "technical",
            "message": "error code 500 when i try to upload files to the platform need urgent assistance"
        },
        {
            "category": "billing",
            "message": "i canceled my subscription but still got charged what is going on here"
        },
        {
            "category": "general",
            "message": "what are your business hours and do you have phone support"
        },
        {
            "category": "technical",
            "message": "can't connect to the vpn after the latest update pls advise"
        },
        {
            "category": "billing",
            "message": "do you have student discount or any promo codes available"
        },
        {
            "category": "complaint",
            "message": "your product is broken and your support team is useless i want a full refund immediately"
        }
    ]
    
    return test_tickets