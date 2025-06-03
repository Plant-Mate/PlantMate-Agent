# from apscheduler.schedulers.background import BackgroundScheduler
# from src.agents.care_suggestion_agent import care_agent
# from src.models.plant_status import PlantStatus
# import atexit
#
# scheduler = BackgroundScheduler()
#
# def generate_daily_care():
#     plant_list = [
#         PlantStatus(name="a", species="蘆薈", last_watered_days=3, temperature=25, humidity=55),
#         PlantStatus(name="b", species="多肉", last_watered_days=1, temperature=27, humidity=50),
#     ]
#
#     for plant in plant_list:
#         result = care_agent.run_sync("give daliy care sugguestion according to status of the plant", deps=plant)
#         print(f"[{plant.name}] 今日建議：{result.output.message}")
#
# scheduler.add_job(generate_daily_care, 'cron', hour=21, minute=3)
#
# def start_scheduler():
#     scheduler.start()
#     print("APScheduler 已啟動")
#     atexit.register(lambda: scheduler.shutdown())
