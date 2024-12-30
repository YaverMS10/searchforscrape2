import flet as ft
import pandas as pd
import openai
import ast
import os
import app

from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('openai_key')

with open('instructions.txt', 'r') as file:
    instruction = file.read()

def scrape(features_dict, page):
    if features_dict['category'] == 'house':
        try:
            status_text_binaaz = ft.Text("Please wait for Bina.az scraping..", color="blue")
            page.add(status_text_binaaz)
            page.update()
            bina_results = app.handle_house_search(features_dict)
            headers = list(bina_results[0].keys())
            table = ft.DataTable(columns=[ft.DataColumn(ft.Text(header)) for header in headers],
                                rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(str(row[key]))) for key in headers]) for row in bina_results])
            page.add(ft.Text("Bina.az Scraping Results", weight="bold", size=28, color="white"))
            page.add(table)
            page.update()
        except:
            page.add(ft.Text("No Bina.az item found for this filter"))

    elif features_dict['category'] == 'other':
        try:
            status_text_tapaz = ft.Text("Please wait for Tap.az scraping..", color="blue")
            page.add(status_text_tapaz)
            page.update()
            tapaz_results = app.handle_other_search(features_dict)

            headers = list(tapaz_results[0].keys())
            table = ft.DataTable(columns=[ft.DataColumn(ft.Text(header)) for header in headers],
                                rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(str(row[key]))) for key in headers]) for row in tapaz_results])
            page.add(ft.Text("Tap.az Scraping Results", weight="bold", size=28, color="white"))
            page.add(table)
            page.update()
        except:
            page.add(ft.Text("No Tap.az item found for this filter"))


        try:
            status_text_instagram = ft.Text("Please wait for Instagram scraping..", color="blue")
            page.add(status_text_instagram)
            page.update()
            instagram_results = app.handle_instagram_search(features_dict)
            
            headers = list(instagram_results[0].keys())
            table = ft.DataTable(columns=[ft.DataColumn(ft.Text(header)) for header in headers],
                                rows=[ft.DataRow(cells=[ft.DataCell(ft.Text(str(row[key]))) for key in headers]) for row in instagram_results])
            page.add(ft.Text("Instagram Scraping Results", weight="bold", size=28, color="white"))
            page.add(table)
            page.update()
        except:
            page.add(ft.Text("No Instagram item found for this filter"))

    try:
        status_text_tapaz.value = ""
    except:
        pass

    try:
        status_text_instagram.value = ""
    except:
        pass

    try:
        status_text_binaaz.value = ""
    except:
        pass
    
    page.update()


def button_clicked(e):
    global tb
    user_input = tb.value
    try:
        response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": instruction},
                        {"role": "user", "content": user_input}])
        features_dict = ast.literal_eval(response['choices'][0]['message']['content'])
        print(features_dict)
        scrape(features_dict, e.page)
    except:
        e.page.add(ft.Text("OpenAI Error"))
        e.page.update()

def main(page:ft.Page):
    global tb
    page.horizontal_alignment = 'center'
    page.vertical_alignment = 'center'
    tb = ft.TextField(label="Enter Desired Item", hint_text="Enter Desired Item")
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(tb, b)

ft.app(main)