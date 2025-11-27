import httpx
import asyncio

from openai import AsyncOpenAI
from openai.types.chat.chat_completion_user_message_param import ChatCompletionUserMessageParam

from database.model import DiagnosticFormTable
from config_data.config import Config, load_config


config: Config = load_config()

proxy = config.proxy


client = AsyncOpenAI(
    api_key=config.openai.token,
    http_client=httpx.AsyncClient(proxy=f'http://{proxy.login}:{proxy.password}@{proxy.ip}:{proxy.port}')
)


async def get_prompt_answer(form_data: DiagnosticFormTable) -> str:
    prompt = f"""
Ты — опытный бизнес-консультант по автоматизации. Проанализируй вводные данные о бизнесе и дай развернутые рекомендации.

Данные о бизнесе:

Ниша и роль: {form_data.niche}
Ключевая проблема: {form_data.pain}
Масштаб проблемы: {form_data.problem}
Текущие инструменты: {form_data.digitalization}
Финансовое влияние: {form_data.finance}
Желаемый результат: {form_data.purpose}

Задача:

Сформулируй 2-3 ключевые рекомендации по автоматизации, основанные на самых болезненных точках клиента.
Укажи, какой может быть потенциальная экономия времени/ресурсов.
В конце ответа обязательно добав следующий блок, точно передающий эту мысль:
Важно: Это — предварительный анализ, основанный на ограниченных данных. Чтобы выявить все скрытые узкие места и разработать детальный пошаговый план автоматизации именно под ваши процессы, необходим глубокий аудит. В его рамках мы проведем полный разбор ваших операций, проанализируем документооборот и дадим готовое решение под ключ. [Предложить записаться на консультацию]
    """
    messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ]
            }
    ]
    response = await client.chat.completions.create(
        model='gpt-4.1-mini',
        messages=messages
    )
    return response.choices[0].message.content.strip()


