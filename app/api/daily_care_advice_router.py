import random
import textwrap

from fastapi import APIRouter
from starlette.responses import JSONResponse

# from app.models.daily_care_advice import SensorDataSummary
# from app.services.agents.care_advice_agent import CareAdviceAgent
from app.models.daily_care_advice import FakeDailyAdvice

router = APIRouter(prefix="/api/agents", tags=["agents"])

# @router.post("/daily-advice")
# def ask_daily_advice(request: SensorDataSummary, agent: CareAdviceAgent):
#     return {"reply": "Hello World"}

@router.post("/daily-advice")
def daily_care_advice():
    advices = [
        textwrap.dedent("""\
                1.是否需要澆水？
                土壤濕度僅有 28%，已低於一般建議的 30–40% 底線，且環境溫度偏高，蒸發速率快，建議立即進行澆水。
                建議澆水量約 150–200 毫升，直至土壤表層（約前 5 公分）充分濕潤為止。
                2.其他備註：
                外部溫度已達 34°C，日中光照強烈，需要避免葉片被灼傷。建議中午 12–14 點之間將植株移到半遮陰處（如室內明亮窗邊或遮陽網下），確保有微風流通。
                晚間若溫度降到 24°C 以下，可考慮將植株稍微移至通風處，避免悶熱積水造成根部缺氧。
            """),
        textwrap.dedent("""\
                1.是否需要澆水？
                土壤濕度已達 65%，屬於偏高範圍，且今日氣溫在 26°C 左右不算太炎熱，暫時不需要澆水。
                建議今天先不要加水，待明早再測試土壤前 3 公分是否低於 40% 再決定。
                2.其他備註：
                現在環境溫度屬溫和多雲或散射光範圍，就算放在窗邊也能滿足光合作用。
                由於土壤偏濕，需注意盆底排水是否順暢，若發現滴水盤有積水，要立即倒掉，以免根部悶濕易生病菌。
            """),
        textwrap.dedent("""\
                1.是否需要澆水？
                土壤濕度 42% 屬於中等偏乾，但溫度只有 19°C（接近晚秋涼爽）時，蒸發較慢，可以暫緩澆水。
                建議今天先不澆，並在晚上或明早再度量濕度：若降到 30–35% 以下再補充約 100 毫升水分即可。
                2.其他備註：
                氣溫 19°C 已經接近較低溫度，且夜間若低於 15°C，沙漠玫瑰易受冷害，建議白天放在東向或南向窗邊接受散射光，夜間可適度移到室內較暖區。
                目前土壤濕度不高，也不宜施肥。若下週需要施肥，等氣溫回升到 24–28°C、土壤濕度約 40–50% 時，再以 1/3 濃度液肥補充養分即可。
            """)
    ]

    return FakeDailyAdvice(advice=random.choice(advices))
