def get_weather(location):
    """
    Simulates getting weather data for a location.
    In a real application, this would call a weather API.
    """
    # This is a mock implementation
    weather_data = {
        "Paris, France": "temperature: 22",
        "London, UK": "temperature: 18",
        "New York, USA": "temperature: 25",
        "Tokyo, Japan": "temperature: 27",
        "Bogotá, Colombia": "temperature: 20"
    }
    
    # Return mock data if location exists, otherwise return a default
    return weather_data.get(location, "temperature: 20") 
