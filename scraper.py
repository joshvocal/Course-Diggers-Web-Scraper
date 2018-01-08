import requests
import sqlite3

COURSE_DIGGER_JSON_URL = "http://www.coursediggers.com/data/{}.json"
SFU_ID = 3


def populate_db(db_conn):
    urls = [COURSE_DIGGER_JSON_URL.format(i) for i in range(1, 10376)]

    for url in urls:

        print("Scraping: " + url)

        course_page = requests.get(url)

        if course_page.status_code == requests.codes.ok:

            course_page_json = course_page.json()

            if course_page_json['metadata']['dataSource']['id'] == SFU_ID:

                course_name = None
                median_grade = None
                fail_percentage = None
                num_students = 0

                if 'name' in course_page_json:
                    course_name = course_page_json['name']

                if 'data' in course_page_json:
                    median_grade = course_page_json['data'][0][0]
                    fail_percentage = course_page_json['data'][0][1]

                for x in range(2, 12):
                    num_students += course_page_json['data'][0][x]

                zero_to_ten = course_page_json['data'][0][2] / num_students * 100
                ten_to_twenty = course_page_json['data'][0][3] / num_students * 100
                twenty_to_thirty = course_page_json['data'][0][4] / num_students * 100
                thirty_to_forty = course_page_json['data'][0][5] / num_students * 100
                forty_to_fifty = course_page_json['data'][0][6] / num_students * 100
                fifty_to_sixty = course_page_json['data'][0][7] / num_students * 100
                sixty_to_seventy = course_page_json['data'][0][8] / num_students * 100
                seventy_to_eighty = course_page_json['data'][0][9] / num_students * 100
                eighty_to_ninety = course_page_json['data'][0][10] / num_students * 100
                ninety_to_hundred = course_page_json['data'][0][11] / num_students * 100

                db_conn.cursor().execute(
                    "INSERT INTO sfu_grades VALUES ('%s', '%s', %.1f, %.1f, %.1f, %.1f, %.1f,"
                    "%.1f, %.1f, %.1f, %.1f, %.1f, %.1f)"
                    % (course_name,
                       median_grade,
                       fail_percentage,
                       zero_to_ten,
                       ten_to_twenty,
                       twenty_to_thirty,
                       thirty_to_forty,
                       forty_to_fifty,
                       fifty_to_sixty,
                       sixty_to_seventy,
                       seventy_to_eighty,
                       eighty_to_ninety,
                       ninety_to_hundred))
                db_conn.commit()


def create_db():
    db_conn = sqlite3.connect('sfu_grades.db')

    db_conn.cursor().execute("""CREATE TABLE sfu_grades (
        course_name TEXT,
        median_grade TEXT,
        fail_rate DOUBLE,
        zero_to_ten DOUBLE,
        ten_to_twenty DOUBLE,
        twenty_to_thirty DOUBLE,
        thirty_to_forty DOUBLE,
        forty_to_fifty DOUBLE,
        fifty_to_sixty DOUBLE,
        sixty_to_seventy DOUBLE,
        seventy_to_eighty DOUBLE,
        eighty_to_ninety DOUBLE,
        ninety_to_hundred DOUBLE)""")

    return db_conn


def main():
    db_conn = create_db()
    populate_db(db_conn)
    db_conn.close()
    print("Finished")


if __name__ == '__main__':
    main()
