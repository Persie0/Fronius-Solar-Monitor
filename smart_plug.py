import logging

# Global variable to track smart plug state
smart_plug_state = False

def initialize_smart_plug(config):
    """
    Initialize the smart plug functionality based on configuration.
    Returns True if smart plug support is enabled and initialized successfully.
    """
    if "smart_plug" not in config or not config["smart_plug"].get("enabled", False):
        return False
    
    try:
        import tinytuya
        logging.info("Smart plug support enabled")
        return True
    except ImportError:
        logging.error("TinyTuya library not installed. Smart plug support disabled.")
        logging.error("Install with: pip install tinytuya")
        return False

def control_smart_plug(config, turn_on=False):
    """
    Controls the smart plug if enabled.
    
    Args:
        config: Configuration dictionary containing smart plug settings
        turn_on: Boolean indicating whether to turn the plug on (True) or off (False)
    """
    global smart_plug_state
    
    # If smart plug is not in config or not enabled, do nothing
    if "smart_plug" not in config or not config["smart_plug"].get("enabled", False):
        return
    
    # If the plug is already in the desired state, do nothing
    if (turn_on and smart_plug_state) or (not turn_on and not smart_plug_state):
        return
    
    try:
        import tinytuya
        
        # Connect to the smart plug
        d = tinytuya.OutletDevice(
            dev_id=config["smart_plug"]["dev_id"],
            address=config["smart_plug"].get("address", "Auto"),
            local_key=config["smart_plug"]["local_key"],
            version=config["smart_plug"].get("version", 3.5)
        )
        
        # Turn on or off based on parameter
        if turn_on:
            d.turn_on()
            smart_plug_state = True
            logging.info("Smart plug turned ON")
        else:
            d.turn_off()
            smart_plug_state = False
            logging.info("Smart plug turned OFF")
            
    except Exception as e:
        logging.error(f"Error controlling smart plug: {e}")