from __future__ import annotations

import json
import re

import schoolopy
from flask import session
from mongoengine import Q

from app.static.python.utils.security import valid_password
from ..classes import *

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


def getLocal():
    if not session["global"]:
        session["global"] = "us"
    return session["global"]


def getText(query):
    dictionary = {
        "Nebulus": {
            "us": "Nebulus",
            "uk": "Nebulus",
            "au": "Nebulus",
            "es": "Nébulus",
            "mx": "Nébulus",
            "cr": "Nébulus",
            "cu": "Nébulus",
            "co": "Nébulus",
            "ar": "Nébulus",
            "it": "Nèbulo",
            "cn": "耐博乐思",
            "tw": "耐博樂思",
            "hk": "耐博樂思",
            "mo": "耐博樂思",
            "jp": "ネビュラス",
            "kr": "네뷸러스",
        },
        "Learning": {
            "us": "Learning",
            "uk": "United Kingdom",
            "au": "Australia",
            "es": "España",
            "mx": "México",
            "cr": "Costa Rica",
            "cu": "Cuba",
            "co": "Colombia",
            "ar": "Argentina",
            "it": "Italia",
            "cn": "中国大陆",
            "tw": "台灣",
            "hk": "香港",
            "mo": "澳門",
            "jp": "日本",
            "kr": "대한민국 사람",
        },
        "A Learning, All In One Experience": {
            "us": "A Learning, All In One Experience",
            "uk": "A Learning, All In One Experience",
            "au": "A Learning, All In One Experience",
            "es": "Una Experiencia de Aprendizaje todo en Uno",
            "mx": "Una Experiencia de Aprendizaje todo en Uno",
            "cr": "Una Experiencia de Aprendizaje todo en Uno",
            "cu": "Una Experiencia de Aprendizaje todo en Uno",
            "co": "Una Experiencia de Aprendizaje todo en Uno",
            "ar": "Una Experiencia de Aprendizaje todo en Uno",
            "cn": "一个有趣，全面的学习平台",
            "tw": "一个有趣，全面的学习平台",
            "hk": "一个有趣，全面的学习平台",
            "mo": "一个有趣，全面的学习平台",
            "kr": "하나의 경험에서 배우는 학습",
        },
        "Nebulus. Education. Redefined.": {
            "us": "Nebulus. Education. Redefined",
            "uk": "Nebulus. Education. Redefined",
            "au": "Nebulus. Education. Redefined",
            "es": "Nébulus. Educación. Redefinida.",
            "mx": "Nébulus. Educación. Redefinida.",
            "cr": "Nébulus. Educación. Redefinida.",
            "cu": "Nébulus. Educación. Redefinida.",
            "co": "Nébulus. Educación. Redefinida.",
            "ar": "Nébulus. Educación. Redefinida.",
            "it": "Nebulo. Istruzione. Ridefinito.",
            "cn": "耐博乐思：创新的教育方式。",
            "tw": "耐博樂思：創新的教育方式。",
            "hk": "耐博樂思：創新的教育方式。",
            "mo": "耐博樂思：創新的教育方式。",
            "jp": "ネビュラス。新しい教育の始まり。",
            "kr": "네뷸러스.  교육.  재정의.",
        },
        "Nebulus helps you have your whole learning experience organized and simple. First, we offer many connections. No more switching between websites. You can connect your Schoology, Google Classroom, and Canvas accounts connected on Nebulus for easy access. You can also stay organized with Nebulus. There is no need to have your papers, documents, assignments, textbooks, calendars, and events all over the place. Everything is organized for you in an easy-to-use way! You can have everything you need for school in one place. Additionally, we understand studying and learning can be difficult. We have tools to organize your studying, organize your materials, make learning fun, and keep you focused! You can use our study timers, test review planning, etc. We have many extensions and integrations to enrich your experience. We have Calculator integrations, a Graphing Calculator, a Dictionary, a Plagarism Checker, a World Map, a Periodic Table, a built-in IDE (Code Editor), and a Document editor (that can edit Word or Google Docs), and much more! We are adding even more features for our Stable release on December 23rd.": {
            "us": "Nebulus helps you have your whole learning experience organized and simple. First, we offer many connections. No more switching between websites. You can connect your Schoology, Google Classroom, and Canvas accounts connected on Nebulus for easy access. You can also stay organized with Nebulus. There is no need to have your papers, documents, assignments, textbooks, calendars, and events all over the place. Everything is organized for you in an easy-to-use way! You can have everything you need for school in one place. Additionally, we understand studying and learning can be difficult. We have tools to organize your studying, organize your materials, make learning fun, and keep you focused! You can use our study timers, test review planning, etc. We have many extensions and integrations to enrich your experience. We have Calculator integrations, a Graphing Calculator, a Dictionary, a Plagarism Checker, a World Map, a Periodic Table, a built-in IDE (Code Editor), and a Document editor (that can edit Word or Google Docs), and much more! We are adding even more features for our Stable release on December 23rd.d",
            "uk": "Nebulus helps you have your whole learning experience organized and simple. First, we offer many connections. No more switching between websites. You can connect your Schoology, Google Classroom, and Canvas accounts connected on Nebulus for easy access. You can also stay organized with Nebulus. There is no need to have your papers, documents, assignments, textbooks, calendars, and events all over the place. Everything is organized for you in an easy-to-use way! You can have everything you need for school in one place. Additionally, we understand studying and learning can be difficult. We have tools to organize your studying, organize your materials, make learning fun, and keep you focused! You can use our study timers, test review planning, etc. We have many extensions and integrations to enrich your experience. We have Calculator integrations, a Graphing Calculator, a Dictionary, a Plagarism Checker, a World Map, a Periodic Table, a built-in IDE (Code Editor), and a Document editor (that can edit Word or Google Docs), and much more! We are adding even more features for our Stable release on December 23rd.",
            "au": "Nebulus helps you have your whole learning experience organized and simple. First, we offer many connections. No more switching between websites. You can connect your Schoology, Google Classroom, and Canvas accounts connected on Nebulus for easy access. You can also stay organized with Nebulus. There is no need to have your papers, documents, assignments, textbooks, calendars, and events all over the place. Everything is organized for you in an easy-to-use way! You can have everything you need for school in one place. Additionally, we understand studying and learning can be difficult. We have tools to organize your studying, organize your materials, make learning fun, and keep you focused! You can use our study timers, test review planning, etc. We have many extensions and integrations to enrich your experience. We have Calculator integrations, a Graphing Calculator, a Dictionary, a Plagarism Checker, a World Map, a Periodic Table, a built-in IDE (Code Editor), and a Document editor (that can edit Word or Google Docs), and much more! We are adding even more features for our Stable release on December 23rd.",
            "es": "Nébulus te ayuda a tener todo tu aprendizaje organizado y simple. Para empezar, ofrecemos muchas conexiones con otros sitios web. Ya no hace falta que cambies entre sitios web. Puedes conectar tus cuentas de Schoology, Google Classroom y Canvas en Nébulus para acceder a ellas fácilmente. También te puedes organizar con Nébulus. No hace falta que tengas todos tus papeles, documentos, tareas, libros de texto, calendarios y eventos por todos lados. ¡Todo está organizado para ti de manera fácil de usar! Puedes tener todo lo que necesitas para la escuela en un lugar. Aparte de eso, entendemos que estudiar y aprender puede ser dificil. ¡Por eso, hemos añadido herramientas que te ayudan a organizar tu estudio, organizar tus materiales, hacer que aprender sea divertido y mantener tu concentración! Puedes usar nuestros temporizadores de estudio, planeadores de trabajo y de revisión de exámenes y mucho más. También contamos con una gran variedad de extensiones e integraciones para enriquecer tu experiencia. ¡Tenemos integraciones que te permiten tener una calculadora, una calculadora gráfica, un diccionario, un comprobador de plagio, un mapamundi, una tabla periódica, un editor de código y un editor de documentos que puede editar Microsoft Word o Google Docs y mucho más! Estamos añadiendo muchos más aspectos para nuestro lanzamiento de la web estable el 23 de diciembre de 2022.",
            "mx": "Nébulus te ayuda a tener todo tu aprendizaje organizado y simple. Para empezar, ofrecemos muchas conexiones con otros sitios web. Ya no hace falta que cambies entre sitios web. Puedes conectar tus cuentas de Schoology, Google Classroom y Canvas en Nébulus para acceder a ellas fácilmente. También te puedes organizar con Nébulus. No hace falta que tengas todos tus papeles, documentos, tareas, libros de texto, calendarios y eventos por todos lados. ¡Todo está organizado para ti de manera fácil de usar! Puedes tener todo lo que necesitas para la escuela en un lugar. Aparte de eso, entendemos que estudiar y aprender puede ser dificil. ¡Por eso, hemos añadido herramientas que te ayudan a organizar tu estudio, organizar tus materiales, hacer que aprender sea divertido y mantener tu concentración! Puedes usar nuestros temporizadores de estudio, planeadores de trabajo y de revisión de exámenes y mucho más. También contamos con una gran variedad de extensiones e integraciones para enriquecer tu experiencia. ¡Tenemos integraciones que te permiten tener una calculadora, una calculadora gráfica, un diccionario, un comprobador de plagio, un mapamundi, una tabla periódica, un editor de código y un editor de documentos que puede editar Microsoft Word o Google Docs y mucho más! Estamos añadiendo muchos más aspectos para nuestro lanzamiento de la web estable el 23 de diciembre de 2022.",
            "cr": "Nébulus te ayuda a tener todo tu aprendizaje organizado y simple. Para empezar, ofrecemos muchas conexiones con otros sitios web. Ya no hace falta que cambies entre sitios web. Puedes conectar tus cuentas de Schoology, Google Classroom y Canvas en Nébulus para acceder a ellas fácilmente. También te puedes organizar con Nébulus. No hace falta que tengas todos tus papeles, documentos, tareas, libros de texto, calendarios y eventos por todos lados. ¡Todo está organizado para ti de manera fácil de usar! Puedes tener todo lo que necesitas para la escuela en un lugar. Aparte de eso, entendemos que estudiar y aprender puede ser dificil. ¡Por eso, hemos añadido herramientas que te ayudan a organizar tu estudio, organizar tus materiales, hacer que aprender sea divertido y mantener tu concentración! Puedes usar nuestros temporizadores de estudio, planeadores de trabajo y de revisión de exámenes y mucho más. También contamos con una gran variedad de extensiones e integraciones para enriquecer tu experiencia. ¡Tenemos integraciones que te permiten tener una calculadora, una calculadora gráfica, un diccionario, un comprobador de plagio, un mapamundi, una tabla periódica, un editor de código y un editor de documentos que puede editar Microsoft Word o Google Docs y mucho más! Estamos añadiendo muchos más aspectos para nuestro lanzamiento de la web estable el 23 de diciembre de 2022.",
            "cu": "Nébulus te ayuda a tener todo tu aprendizaje organizado y simple. Para empezar, ofrecemos muchas conexiones con otros sitios web. Ya no hace falta que cambies entre sitios web. Puedes conectar tus cuentas de Schoology, Google Classroom y Canvas en Nébulus para acceder a ellas fácilmente. También te puedes organizar con Nébulus. No hace falta que tengas todos tus papeles, documentos, tareas, libros de texto, calendarios y eventos por todos lados. ¡Todo está organizado para ti de manera fácil de usar! Puedes tener todo lo que necesitas para la escuela en un lugar. Aparte de eso, entendemos que estudiar y aprender puede ser dificil. ¡Por eso, hemos añadido herramientas que te ayudan a organizar tu estudio, organizar tus materiales, hacer que aprender sea divertido y mantener tu concentración! Puedes usar nuestros temporizadores de estudio, planeadores de trabajo y de revisión de exámenes y mucho más. También contamos con una gran variedad de extensiones e integraciones para enriquecer tu experiencia. ¡Tenemos integraciones que te permiten tener una calculadora, una calculadora gráfica, un diccionario, un comprobador de plagio, un mapamundi, una tabla periódica, un editor de código y un editor de documentos que puede editar Microsoft Word o Google Docs y mucho más! Estamos añadiendo muchos más aspectos para nuestro lanzamiento de la web estable el 23 de diciembre de 2022.",
            "co": "Nébulus te ayuda a tener todo tu aprendizaje organizado y simple. Para empezar, ofrecemos muchas conexiones con otros sitios web. Ya no hace falta que cambies entre sitios web. Puedes conectar tus cuentas de Schoology, Google Classroom y Canvas en Nébulus para acceder a ellas fácilmente. También te puedes organizar con Nébulus. No hace falta que tengas todos tus papeles, documentos, tareas, libros de texto, calendarios y eventos por todos lados. ¡Todo está organizado para ti de manera fácil de usar! Puedes tener todo lo que necesitas para la escuela en un lugar. Aparte de eso, entendemos que estudiar y aprender puede ser dificil. ¡Por eso, hemos añadido herramientas que te ayudan a organizar tu estudio, organizar tus materiales, hacer que aprender sea divertido y mantener tu concentración! Puedes usar nuestros temporizadores de estudio, planeadores de trabajo y de revisión de exámenes y mucho más. También contamos con una gran variedad de extensiones e integraciones para enriquecer tu experiencia. ¡Tenemos integraciones que te permiten tener una calculadora, una calculadora gráfica, un diccionario, un comprobador de plagio, un mapamundi, una tabla periódica, un editor de código y un editor de documentos que puede editar Microsoft Word o Google Docs y mucho más! Estamos añadiendo muchos más aspectos para nuestro lanzamiento de la web estable el 23 de diciembre de 2022.",
            "ar": "Nébulus te ayuda a tener todo tu aprendizaje organizado y simple. Para empezar, ofrecemos muchas conexiones con otros sitios web. Ya no hace falta que cambies entre sitios web. Puedes conectar tus cuentas de Schoology, Google Classroom y Canvas en Nébulus para acceder a ellas fácilmente. También te puedes organizar con Nébulus. No hace falta que tengas todos tus papeles, documentos, tareas, libros de texto, calendarios y eventos por todos lados. ¡Todo está organizado para ti de manera fácil de usar! Puedes tener todo lo que necesitas para la escuela en un lugar. Aparte de eso, entendemos que estudiar y aprender puede ser dificil. ¡Por eso, hemos añadido herramientas que te ayudan a organizar tu estudio, organizar tus materiales, hacer que aprender sea divertido y mantener tu concentración! Puedes usar nuestros temporizadores de estudio, planeadores de trabajo y de revisión de exámenes y mucho más. También contamos con una gran variedad de extensiones e integraciones para enriquecer tu experiencia. ¡Tenemos integraciones que te permiten tener una calculadora, una calculadora gráfica, un diccionario, un comprobador de plagio, un mapamundi, una tabla periódica, un editor de código y un editor de documentos que puede editar Microsoft Word o Google Docs y mucho más! Estamos añadiendo muchos más aspectos para nuestro lanzamiento de la web estable el 23 de diciembre de 2022.",
            "cn": "耐博乐思会让您的整个学习体验变得既简单，又有秩序。首先，我们会给予许多网站联系。您不用再在网站之间反复阅览了。比如，您可以在耐博乐思平台上轻松地连接像Schoology, Canvas, 或Google Classroom等各种学习网站。其次，您也可以在耐博乐思平台上有秩序地学习。您不再需要将文档、论文、作业、教科书、时间表、事件等所有任务摊得到处都是了。所有元素都会为您整理成一个方便快捷的方式！您可以将所有学校需要的元素全都收集在同一个地方。除此之外，我们也十分理解学习可能会很枯燥。针对这个，我们也有许多工具可以帮您学习、整理资料、让学习变快乐、同时也让您专注于学习！您可以选择使用我们的学习时钟、考试周计划表、等。我们也有许多扩展集成去丰富您的使用经历。我们包括计算机集成、图表计算机集成、字典扩展、抄袭检查器扩展、世界地图、元素周期表、集成代码编辑器、可以跨编辑器编写的文档编辑器、等许多其他的工具！我们也会在12月23号即将发布的的稳定更新上增加更多的功能选项！",
            "tw": "耐博樂思會讓您的整個學習體驗變得既簡單，又有秩序。首先，我們會給予許多網站聯繫。您不用再在網站之間反复閱覽了。比如，您可以在耐博樂思平台上輕鬆地連接像Schoology, Canvas, 或Google Classroom等各種學習網站。其次，您也可以在耐博樂思平台上有秩序地學習。您不再需要將文檔、論文、作業、教科書、時間表、事件等所有任務攤得到處都是了。所有元素都會為您整理成一個方便快捷的方式！您可以將所有學校需要的元素全都收集在同一個地方。除此之外，我們也十分理解學習可能會很枯燥。針對這個，我們也有許多工具可以幫您學習、整理資料、讓學習變快樂、同時也讓您專注於學習！您可以選擇使用我們的學習時鐘、考試週計劃表、等。我們也有許多擴展集成去豐富您的使用經歷。我們包括計算機集成、圖表計算機集成、字典擴展、抄襲檢查器擴展、世界地圖、元素週期表、集成代碼編輯器、可以跨編輯器編寫的文檔編輯器、等許多其他的工具！我們也會在12月23號即將發布的的穩定更新上增加更多的功能選項！",
            "hk": "耐博樂思會讓您的整個學習體驗變得既簡單，又有秩序。首先，我們會給予許多網站聯繫。您不用再在網站之間反复閱覽了。比如，您可以在耐博樂思平台上輕鬆地連接像Schoology, Canvas, 或Google Classroom等各種學習網站。其次，您也可以在耐博樂思平台上有秩序地學習。您不再需要將文檔、論文、作業、教科書、時間表、事件等所有任務攤得到處都是了。所有元素都會為您整理成一個方便快捷的方式！您可以將所有學校需要的元素全都收集在同一個地方。除此之外，我們也十分理解學習可能會很枯燥。針對這個，我們也有許多工具可以幫您學習、整理資料、讓學習變快樂、同時也讓您專注於學習！您可以選擇使用我們的學習時鐘、考試週計劃表、等。我們也有許多擴展集成去豐富您的使用經歷。我們包括計算機集成、圖表計算機集成、字典擴展、抄襲檢查器擴展、世界地圖、元素週期表、集成代碼編輯器、可以跨編輯器編寫的文檔編輯器、等許多其他的工具！我們也會在12月23號即將發布的的穩定更新上增加更多的功能選項！",
            "mo": "耐博樂思會讓您的整個學習體驗變得既簡單，又有秩序。首先，我們會給予許多網站聯繫。您不用再在網站之間反复閱覽了。比如，您可以在耐博樂思平台上輕鬆地連接像Schoology, Canvas, 或Google Classroom等各種學習網站。其次，您也可以在耐博樂思平台上有秩序地學習。您不再需要將文檔、論文、作業、教科書、時間表、事件等所有任務攤得到處都是了。所有元素都會為您整理成一個方便快捷的方式！您可以將所有學校需要的元素全都收集在同一個地方。除此之外，我們也十分理解學習可能會很枯燥。針對這個，我們也有許多工具可以幫您學習、整理資料、讓學習變快樂、同時也讓您專注於學習！您可以選擇使用我們的學習時鐘、考試週計劃表、等。我們也有許多擴展集成去豐富您的使用經歷。我們包括計算機集成、圖表計算機集成、字典擴展、抄襲檢查器擴展、世界地圖、元素週期表、集成代碼編輯器、可以跨編輯器編寫的文檔編輯器、等許多其他的工具！我們也會在12月23號即將發布的的穩定更新上增加更多的功能選項！",
            "kr": "네뷸러스 를 사용하면 전체 학습 경험을 체계적이고 간단하게 만들 수 있습니다. 첫째, 우리는 많은 연결을 제공합니다. 더 이상 웹사이트 간에 전환할 필요가 없습니다. 네뷸러스에 연결된 Schoology, Google 클래스룸 및 Canvas 계정을 연결하여 쉽게 액세스할 수 있습니다. 네뷸러스로 정리를 유지할 수도 있습니다. 서류, 문서, 과제, 교과서, 달력 및 이벤트를 여기저기에 둘 필요가 없습니다. 모든 것이 사용하기 쉬운 방식으로 구성되어 있습니다! 학교에 필요한 모든 것을 한 곳에서 받을 수 있습니다. 또한 우리는 공부와 학습이 어려울 수 있음을 이해합니다. 학습을 정리하고, 자료를 정리하고, 학습을 재미있게 만들고, 집중할 수 있는 도구가 있습니다! 학습 타이머, 시험 검토 계획 등을 사용할 수 있습니다. 경험을 풍부하게 하기 위해 많은 확장 및 통합이 있습니다. 계산기 통합, 그래프 계산기, 사전, 표절 검사기, 세계 지도, 주기율표, 내장 IDE(코드 편집기) 및 문서 편집기(Word 또는 Google 문서를 편집할 수 있음) 및 많은 기능이 있습니다. 더! 12월 23일 공개 버전 릴리스에 더 많은 기능을 추가하고 있습니다.",
        },
        "Login": {
            "cn": "登录",
        },
        "Signup": {
            "cn": "注册",
        },
        "Sign Up": {
            "cn": "注册",
        },
        "Launch Nebulus": {
            "cn": "启动耐博乐思",
        },
        "Watch Our Event": {
            "cn": "观看我们的活动",
        },
        "Get Started": {
            "cn": "开始使用！",
        },
        "Learning, All In One": {
            "us": "Learning, All In One",
            "uk": "Learning, All In One",
            "au": "Learning, All In One",
            "es": "Todo tu aprendizaje en un sitio",
            "mx": "Todo tu aprendizaje en un sitio",
            "cr": "Todo tu aprendizaje en un sitio",
            "cu": "Todo tu aprendizaje en un sitio",
            "co": "Todo tu aprendizaje en un sitio",
            "ar": "Todo tu aprendizaje en un sitio",
            "cn": "有趣、全面地学习",
        },
        "Connect all of Learning": {
            "us": "Connect all of Learning",
            "uk": "Connect all of Learning",
            "au": "Connect all of Learning",
            "es": "Conecta todo tu aprendizaje",
            "mx": "Conecta todo tu aprendizaje",
            "cr": "Conecta todo tu aprendizaje",
            "cu": "Conecta todo tu aprendizaje",
            "co": "Conecta todo tu aprendizaje",
            "ar": "Conecta todo tu aprendizaje",
            "cn": "连接所有的学习方式",
        },
        "No more switching between websites. Get your Schoology, Google Classroom, and Canvas accounts connected today.": {
            "us": "No more switching between websites. Get your Schoology, Google Classroom, and Canvas accounts connected today.",
            "uk": "No more switching between websites. Get your Schoology, Google Classroom, and Canvas accounts connected today.",
            "au": "No more switching between websites. Get your Schoology, Google Classroom, and Canvas accounts connected today.",
            "es": "No cambies más entre sitios web. Conecta tus cuentas de Schoology, Google Classroom y Canvas hoy.",
            "mx": "No cambies más entre sitios web. Conecta tus cuentas de Schoology, Google Classroom y Canvas hoy.",
            "cr": "No cambies más entre sitios web. Conecta tus cuentas de Schoology, Google Classroom y Canvas hoy.",
            "cu": "No cambies más entre sitios web. Conecta tus cuentas de Schoology, Google Classroom y Canvas hoy.",
            "co": "No cambies más entre sitios web. Conecta tus cuentas de Schoology, Google Classroom y Canvas hoy.",
            "ar": "No cambies más entre sitios web. Conecta tus cuentas de Schoology, Google Classroom y Canvas hoy.",
            "cn": "您不需要继续在网站之间切换。将您的Schoology. Google Classroom, 与 Canvas账户全部连接到耐博乐思就可以了。",
        },
        "Organize your Learning Experience": {
            "us": "Organize your learning experience",
            "uk": "Organize your learning experience",
            "au": "Organize your learning experience",
            "es": "Organiza tu experiencia de aprendizaje",
            "mx": "Organiza tu experiencia de aprendizaje",
            "cr": "Organiza tu experiencia de aprendizaje",
            "cu": "Organiza tu experiencia de aprendizaje",
            "co": "Organiza tu experiencia de aprendizaje",
            "ar": "Organiza tu experiencia de aprendizaje",
            "cn": "规整您的学习经历",
        },
        "With Nebulus, there is no need to have your papers, documents, assignments, textbooks, and events be all over the place. With Nebulus, everything is organized for you in an easy-to-use way!": {
            "us": "With Nebulus, there is no need to have your papers, documents, assignments, textbooks, and events be all over the place. With Nebulus, everything is organized for you in an easy-to-use way!",
            "uk": "With Nebulus, there is no need to have your papers, documents, assignments, textbooks, and events be all over the place. With Nebulus, everything is organized for you in an easy-to-use way!",
            "au": "With Nebulus, there is no need to have your papers, documents, assignments, textbooks, and events be all over the place. With Nebulus, everything is organized for you in an easy-to-use way!",
            "es": "Con Nébulus, no hay necesidad de tener todos tus papeles, documentos, tareas, libros de texto y eventos por todos lados. ¡Con Nébulus, todo está organizado para ti de manera fácil de usar!",
            "mx": "Con Nébulus, no hay necesidad de tener todos tus papeles, documentos, tareas, libros de texto y eventos por todos lados. ¡Con Nébulus, todo está organizado para ti de manera fácil de usar!",
            "cr": "Con Nébulus, no hay necesidad de tener todos tus papeles, documentos, tareas, libros de texto y eventos por todos lados. ¡Con Nébulus, todo está organizado para ti de manera fácil de usar!",
            "cu": "Con Nébulus, no hay necesidad de tener todos tus papeles, documentos, tareas, libros de texto y eventos por todos lados. ¡Con Nébulus, todo está organizado para ti de manera fácil de usar!",
            "co": "Con Nébulus, no hay necesidad de tener todos tus papeles, documentos, tareas, libros de texto y eventos por todos lados. ¡Con Nébulus, todo está organizado para ti de manera fácil de usar!",
            "ar": "Con Nébulus, no hay necesidad de tener todos tus papeles, documentos, tareas, libros de texto y eventos por todos lados. ¡Con Nébulus, todo está organizado para ti de manera fácil de usar!",
            "cn": "有了耐博乐思，您的论文、文档、作业、教科书和活动就不必到处乱窜了。 使用 耐博乐思，一切都以易于使用的方式为您安排妥当！",
        },
        "Make Learning Easier": {
            "us": "Make Learning Easier",
            "uk": "Make Learning Easier",
            "au": "Make Learning Easier",
            "es": "Haz tu aprendizaje más fácil",
            "mx": "Haz tu aprendizaje más fácil",
            "cr": "Haz tu aprendizaje más fácil",
            "cu": "Haz tu aprendizaje más fácil",
            "co": "Haz tu aprendizaje más fácil",
            "ar": "Haz tu aprendizaje más fácil",
            "cn": "让学习更简单和轻松",
        },
        "We have tools to organize your studying, organize your materials, make learning fun, and keep you focused!": {
            "us": "We have tools to organize your studying, organize your materials, make learning fun, and keep you focused!",
            "uk": "We have tools to organize your studying, organize your materials, make learning fun, and keep you focused!",
            "au": "We have tools to organize your studying, organize your materials, make learning fun, and keep you focused!",
            "es": "¡Tenemos herramientas para organizar tu estudio y tus materiales, hacer que aprender sea divertido y mantener tu concentración!",
            "mx": "¡Tenemos herramientas para organizar tu estudio y tus materiales, hacer que aprender sea divertido y mantener tu concentración!",
            "cr": "¡Tenemos herramientas para organizar tu estudio y tus materiales, hacer que aprender sea divertido y mantener tu concentración!",
            "cu": "¡Tenemos herramientas para organizar tu estudio y tus materiales, hacer que aprender sea divertido y mantener tu concentración!",
            "co": "¡Tenemos herramientas para organizar tu estudio y tus materiales, hacer que aprender sea divertido y mantener tu concentración!",
            "ar": "¡Tenemos herramientas para organizar tu estudio y tus materiales, hacer que aprender sea divertido y mantener tu concentración!",
            "cn": "我们拥有可以许多工具可以帮助您学习，整理资料，让学习变得有趣，并且帮助您保持专注！",
        },
        "Start Now!": {
            "us": "Start Now!",
            "uk": "Start Now!",
            "au": "Start Now!",
            "es": "¡Comienza ahora!",
            "mx": "¡Comienza ahora!",
            "cr": "¡Comienza ahora!",
            "cu": "¡Comienza ahora!",
            "co": "¡Comienza ahora!",
            "ar": "¡Comienza ahora!",
            "cn": "开始使用！",
        },
        "About": {
            "cn": "关于",
        },
        "Pricing": {"cn": "价钱"},
        "Change Language": {"cn": "改变语言"},
        "With Nebulus, have your whole learning experience": {"cn": "耐博乐思会让您的学习经历既有"},
        "organized": {
            "cn": "秩序",
        },
        "and": {
            "cn": "、又",
        },
        "simple": {"cn": "简单方便"},
        "All it takes is one": {
            "cn": "您所需的仅仅是一个",
        },
        "Nebulus Account": {
            "cn": "耐博乐思账号",
        },
        "New to Nebulus?": {"cn": "新手指南?"},
        "Forgot password?": {"cn": "忘记密码？"},
        "Reset": {"cn": "重制"},
        "Or, Sign in with Your Apps:": {"cn": "或者，使用其它应用登录："},
        "Sign up Now": {
            "cn": "现在注册",
        },
        "Password": {
            "cn": "密码",
        },
        "Please enter a password": {
            "cn": "请输入您的密码！",
        },
        "Welcome back to Nebulus! Enter your username please.": {
            "cn": "欢迎回到耐博乐思！请输入您的用户名。",
        },
        "Username": {"cn": "用户名"},
        "Email": {
            "cn": "邮箱",
        },
        "Existing Member?": {
            "cn": "已注册账户？",
        },
        "Prepare for a brighter future in your education with Nebulus!  It's free and it always will be.": {
            "cn": "准备好与耐博乐思一起在您的学习过程中开启一个更美好的未来！",
        },
        "Restart": {
            "cn": "重新输入",
        },
        "Next": {
            "cn": "下一步",
        },
        "Previous": {
            "cn": "前一步",
        },
        "Join": {"cn": "开始用耐博乐思！"},
        "Confirm Password": {
            "cn": "确认密码",
        },
        "Welcome to Nebulus! Please enter an Email!": {"cn": " 欢迎来到耐博乐思！请输入用户名。"},
        "Please enter a Username!": {
            "cn": "请输入用户名。",
        },
        "Please enter a password!": {"cn": "请输入密码！"},
        "Please confirm your password!": {
            "cn": "请确认您的密码！",
        },
    }

    try:
        return dictionary[query][getLocal()]
    except:
        return query


def getAssignment(assignment_id: str) -> Assignment:
    assignment = Assignment.objects(id=assignment_id).first()
    return assignment

def getNebulusDocument(document_id: str) -> NebulusDocument:
    document = NebulusDocument.objects(id=document_id).first()
    return document

def getEvent(event_id: str) -> Event:
    event = Event.objects(pk=event_id).first()
    return event


def getGrades(grades_id: str) -> Grades:
    grades = Grades.objects(pk=grades_id).first()
    return grades


def getDocumentFile(document_file_id: str) -> DocumentFile:
    document_file = DocumentFile.objects(pk=document_file_id).first()
    return document_file


def getFolder(folder_id: str) -> Folder:
    folder = Folder.objects(pk=folder_id).first()
    return folder


def get_user_courses(user_id: str) -> list[Course]:
    user = find_user(pk=user_id)
    return Course.objects(authorizedUsers=user)


def search_user(query: str, ignore_id: str = None) -> list[User]:
    if ignore_id:
        return User.objects(username__istartswith=query, id__ne=ignore_id).only(
            "id", "username", "email", "avatar", "_cls"
        )[:10]
    else:
        return User.objects(username__istartswith=query).only(
            "id", "username", "email", "avatar", "_cls"
        )[:10]
    # return User.objects.filter(username__contains=query)._query


def search_within_course(query: str, course_id: str):
    assignments = Assignment.objects(course_id=course_id, title__contains=query)
    events = Event.objects(course_id=course_id, title__contains=query)
    document_file = DocumentFile.objects(course_id=course_id, title__contains=query)


def find_courses(_id: str):
    course = Course.objects(pk=_id)
    if not course:
        raise KeyError("Course not found")
    return course[0]


def find_user(**kwargs) -> User | None:
    data = {k: v for k, v in kwargs.items() if v is not None}
    user = User.objects(**data).first()
    if not user:
        raise KeyError("User not found")

    return user


def find_folder(**kwargs) -> Folder | None:
    folder = Folder.objects(**kwargs).first()
    if not folder:
        print(folder)
        raise KeyError("Folder not found")
    return folder


def find_document(**kwargs) -> Document | None:
    document = DocumentFile.objects(**kwargs).first()
    if not document:
        print(document)
        raise KeyError("User not found")
    return document


def getSchoology(**kwargs) -> list[Schoology] | None:
    try:
        return find_user(**kwargs).schoology
    except KeyError:
        return


def getClassroom(
    userID: str = None, username: str = None, email: str = None
) -> GoogleClassroom:
    return find_user(id=userID, username=username, email=email).gclassroom


def getSpotify(userID: str = None, username: str = None, email: str = None) -> Spotify:
    return find_user(id=userID, username=username, email=email).spotify


def getSpotifyCache(
    userID: str = None, username: str = None, email: str = None
) -> Spotify | None:
    try:
        return find_user(
            id=userID, username=username, email=email
        ).spotify.Spotify_cache
    except:
        return None


def checkSchoology(_id: int):
    user = find_user(id=_id)
    return str(user and user.schoology).lower()


def check_type(o):
    try:
        a = find_folder(**o)
        if a is None:
            return "document"
        else:
            return "folder"
    except:
        return "document"


def check_password_username(username, password):
    validuser = "false"
    valid_pass = "false"
    try:
        if re.fullmatch(regex, username):
            user = find_user(email=username)
            validuser = "true"
        else:
            user = find_user(username=username)
            validuser = "true"
    except KeyError:
        return "false-false"

    if valid_password(user.password, password):
        valid_pass = "true"
    return f"{validuser}-{valid_pass}"


def get_announcement(announcement_id: str) -> Announcement:
    announcement = Announcement.objects(pk=announcement_id).first()
    return announcement


def get_folders(parent_id: int = None, course_id: int = None) -> list[Folder]:
    if not parent_id and not course_id:
        raise ValueError("Must provide either parent_id or course_id")

    if course_id:
        return find_courses(course_id).folders
    else:
        return find_folder(id=parent_id).subfolders


def sortByDate(obj):
    return obj.date.date() if obj._cls == "Event" else obj.due.date()


def sortByDateTime(obj):
    return obj.date if obj._cls == "Event" else obj.due


def sort_course_events(user_id: str, course_id: int):
    courses = get_user_courses(user_id)
    course = None
    for i in courses:
        if str(i.id) == str(course_id):
            course = i
            break
    courses = [course]

    events = Event.objects(course__in=courses)
    announcements = Announcement.objects(course__in=courses)
    assignments = Assignment.objects(course__in=courses)
    assessments = Assessment.objects(course__in=courses)
    from itertools import chain, groupby

    events_assessments_assignments = list(chain(events, assignments, assessments))
    sorted_events = sorted(
        events_assessments_assignments, key=lambda obj: sortByDateTime(obj)
    )
    dates = dict(
        {
            key: list(result)
            for key, result in groupby(
                sorted_events, key=lambda obj: sortByDateTime(obj)
            )
        }
    )

    sorted_announcements = sorted(announcements, key=lambda obj: obj.date)
    announcements = dict(
        reversed(
            list(
                {
                    key: list(result)
                    for key, result in groupby(
                        sorted_announcements, key=lambda obj: obj.date.date()
                    )
                }.items()
            )
        )
    )

    return [announcements, dates]


def sort_user_events(user_id: str, maxDays=5, maxEvents=16):
    courses = get_user_courses(user_id)
    events = Event.objects(course__in=courses)
    announcements = Announcement.objects(course__in=courses)
    assignments = Assignment.objects(course__in=courses)
    assessments = Assessment.objects(course__in=courses)
    from itertools import chain, groupby

    events_assessments_assignments = list(chain(events, assignments, assessments))
    sorted_events = reversed(
        sorted(
            events_assessments_assignments[:maxEvents],
            key=lambda obj: sortByDateTime(obj),
        )
    )

    dates = dict(
        {
            key: list(result)
            for key, result in groupby(
                sorted_events, key=lambda obj: sortByDateTime(obj)
            )
        }
    )

    sorted_announcements = sorted(announcements, key=lambda obj: obj.date)
    announcements = dict(
        reversed(
            list(
                {
                    key: list(result)
                    for key, result in groupby(
                        sorted_announcements, key=lambda obj: obj.date.date()
                    )
                }.items()
            )[-maxDays:]
        )
    )

    return [announcements, dates]

    # events_assessments_assignments = events | assignments | assessments


def unsorted_user_events(user_id: str) -> list[list]:
    courses = get_user_courses(user_id)
    events = Event.objects(course__in=courses)
    announcements = Announcement.objects(course__in=courses)
    assignments = Assignment.objects(course__in=courses)
    assessments = Assessment.objects(course__in=courses)
    from itertools import chain

    events_assessments_assignments = list(chain(events, assignments, assessments))
    announcements = list(reversed(announcements))
    return [
        announcements,
        sorted(events_assessments_assignments, key=lambda obj: sortByDateTime(obj)),
    ]


def getSchoologyAuth(user_id) -> schoolopy.Schoology | None:
    schoology = getSchoology(id=user_id)
    if not schoology:
        return

    schoology = schoology[0]
    request_token = schoology.Schoology_request_token
    request_token_secret = schoology.Schoology_request_secret
    access_token = schoology.Schoology_access_token
    access_token_secret = schoology.Schoology_access_secret
    link = schoology.schoologyDomain
    key = schoology.apikey
    secret = schoology.apisecret
    auth = schoolopy.Auth(
        key,
        secret,
        domain=link,
        three_legged=True,
        request_token=request_token,
        request_token_secret=request_token_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    auth.authorize()
    sc = schoolopy.Schoology(auth)
    sc.limit = 5

    return sc


def check_signup_user(username) -> str:
    if User.objects(username=username):
        return "false"
    return "true"


def check_signup_email(email) -> str:
    if User.objects(email=email):
        return "false"
    return "true"


def check_duplicate_schoology(schoology_email) -> str:
    if User.objects(schoology__schoologyEmail=schoology_email):
        return "true"
    return "false"


def getChat(chat_id: str):
    chat = Chat.objects.get(pk=chat_id)
    if not chat:
        raise KeyError("Invalid Chat ID")

    return chat


def getPlanner(user_id: str):
    planner = find_user(id=user_id).planner
    if not planner:
        return {}

    return {
        "name": planner.name,
        "saveData": planner.saveData,
        "periods": planner.periods,
        "lastEdited": planner.lastEdited,
    }


def getDocument(document_id: str):  # Nebulus Document
    doc = NebulusDocument.objects(pk=document_id)
    if not doc:
        raise KeyError("Invalid Document ID")
    return doc


def search(keyword: str, username: str):
    user = User.objects(username=username).first()
    users = search_user(keyword)
    pipeline1 = [
        {"$match": {"title": {"$regex": f"^{keyword}", "$options": "i"}}},
        {
            "$lookup": {
                "from": Course._get_collection_name(),
                "localField": "course",
                "foreignField": "_id",
                "as": "course",
            }
        },
        {"$match": {"course.authorizedUsers": user.pk}},
        {"$project": {"title": 1, "_id": 1, "_cls": 1}},
    ]
    courses = Course.objects(Q(authorizedUsers=user.id) & Q(name__istartswith=keyword))[
        :10
    ]
    chats = Chat.objects(Q(owner=user.id) & Q(title__istartswith=keyword))[:10]
    NebulusDocuments = NebulusDocument.objects(
        Q(authorizedUsers=user.id) & Q(name__istartswith=keyword)
    )[:10]

    events = list(Event.objects().aggregate(pipeline1))
    assignments = list(Assignment.objects().aggregate(pipeline1))
    announcements = list(Announcement.objects().aggregate(pipeline1))
    documents = list(DocumentFile.objects.aggregate(pipeline1))
    return (
        courses,
        documents,
        chats,
        events,
        assignments,
        announcements,
        NebulusDocuments,
        users,
    )


def search_course(keyword: str, course: str):
    course = Course.objects(id=course).first()
    pipeline1 = [
        {"$match": {"title": {"$regex": f"^{keyword}", "$options": "i"}}},
        {
            "$lookup": {
                "from": Course._get_collection_name(),
                "localField": "course",
                "foreignField": "_id",
                "as": "course",
            }
        },
        {"$match": {"course.id": course}},
        {"$project": {"title": 1, "_id": 1, "_cls": 1}},
    ]

    events = list(Event.objects().aggregate(pipeline1))
    assignments = list(Assignment.objects().aggregate(pipeline1))
    announcements = list(Announcement.objects().aggregate(pipeline1))
    documents = list(DocumentFile.objects.aggregate(pipeline1))
    return (
        documents,
        events,
        assignments,
        announcements,
        # NebulusDocuments,
    )


def getUserChats(user_id, required_fields: list):
    chats = Chat.objects(members__user=user_id).only(*required_fields)
    return chats


def loadChats(user_id: str, current_index, initial_amount, required_fields):
    chats = json.loads(getUserChats(user_id, required_fields).to_json())

    chats = sorted(chats, key=lambda x: x["lastEdited"]["$date"], reverse=True)

    if len(chats) < current_index + initial_amount:
        initial_amount = len(chats) - current_index

    chats = chats[current_index : (current_index + initial_amount)]
    for chat in chats:
        if len(chat["members"]) == 2:
            for x, member in enumerate(chat["members"]):
                chat["members"][x]["user"] = json.loads(
                    User.objects.only(
                        "id", "chatProfile", "username", "avatar.avatar_url"
                    )
                    .get(pk=member["user"])
                    .to_json()
                )
                chat["members"][x]["unread"] = str(chat["members"][x]["unread"])
            chat["owner"] = list(
                filter(lambda x: x["user"]["_id"] == chat["owner"], chat["members"])
            )[0]

    print(chats)
    return chats


def get_friends(user_id):
    user = find_user(pk=user_id)
    try:
        friends = user.chatProfile.friends
    except:
        friends = None
    return friends


def get_blocks(user_id):
    user = find_user(pk=user_id)
    try:
        blocked = user.chatProfile.blocked
    except:
        blocked = None
    return blocked
