import requests
import csv
from bs4 import BeautifulSoup

def extract_data_from_div(div):
    """Extracts relevant information from a 'cupHisNew' div."""
    bet_slip_number = div.find('b').text.strip()
    time = div.find('time').text.strip()
    bet_label = div.find('label', class_='hisName').text.strip()
    odds = div.find('div', class_='hisCof').text.strip()
    return bet_slip_number, time, bet_label, odds

def extract_data_from_table_row(row):
    """Extracts data from a table row, handling potential incomplete data."""
    if len(row.find_all('td')) >= 5:
        game = row.find_all('td')[1].text.strip()
        bet_type = row.find_all('td')[2].text.strip()
        odds = row.find_all('td')[3].text.strip()
        status = row.find_all('td')[4].text.strip()
        return game, bet_type, odds, status
    else:
        return None

def parse_html_file(file_path):
    """Parses an HTML file and returns a BeautifulSoup object."""
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    return BeautifulSoup(html_content, 'html.parser')

def process_bet_slip(cup_his_new_div, index, csv_writer):
    """Processes a single bet slip div and writes its data to the CSV."""
    bet_slip_number, time, bet_label, odds = extract_data_from_div(cup_his_new_div)

    for row in cup_his_new_div.find('table', class_='table_prop').find_all('tr')[2:]:
        row_data = extract_data_from_table_row(row)
        if row_data:
            game, bet_type, odds, status = row_data
            csv_writer.writerow([bet_slip_number, bet_type, game, odds, status])
        else:
            print(f"Bet Slip {index} - Incomplete row data")

def main():
    local_html_file_path = '/home/fiend/Srcode/betpro/data/history_332640219.html'
    output_csv_file = 'xbet_history.csv'

    soup = parse_html_file(local_html_file_path)

    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Bet Slip', 'Bet Type', 'Game', 'Odds', 'Status'])

        for index, cup_his_new_div in enumerate(soup.find_all('div', class_='cupHisNew'), start=1):
            process_bet_slip(cup_his_new_div, index, csv_writer)
            
if __name__ == '__main__':
    main()


