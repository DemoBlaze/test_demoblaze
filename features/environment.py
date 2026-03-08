from config.drivers import get_driver


def before_scenario(context, scenario):
    """Initialise le driver uniquement pour les scénarios @ui."""
    context.driver = None
    if "ui" in scenario.effective_tags:
        context.driver = get_driver()


def after_scenario(context, scenario):
    """Ferme le driver seulement s'il a été ouvert."""
    if hasattr(context, "driver") and context.driver is not None:
        if scenario.status == "failed":
            screenshot_path = (
                f"reports/screenshots/{scenario.name.replace(' ', '_')}.png"
            )
            try:
                context.driver.save_screenshot(screenshot_path)
                print(f"\n📸 Screenshot : {screenshot_path}")
            except Exception:
                pass
        context.driver.quit()
        context.driver = None
