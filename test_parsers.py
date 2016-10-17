import unittest
from parsers import groups_parser, student_list_parser, student_parser


class ParserTestCase(unittest.TestCase):
    def test_groups_parser(self):
        text = '''
            <select id="group" name="group">
                <option value=""/>
                <option value="15798">АЭМББТ</option>
                <option value="35568">Б8102</option>
                <option value="2107">Б8103а</option>
                <option value="3240" selected="selected">мастер-класс</option>
                <option value="-">без группы</option>
            </select>'''
        data = [
            {'id': 15798, 'name': 'АЭМББТ'},
            {'id': 35568, 'name': 'Б8102'},
            {'id': 2107, 'name': 'Б8103а'},
            {'id': 3240, 'name': 'мастер-класс'},
        ]

        self.assertEqual(groups_parser(text), data)

    def test_students_parser(self):
        text = '''
            <table class="works">
                <tr>
                    <th>N</th><th>Ф. И. О.</th><th>Группы</th>
                </tr><tr>
                    <td><a href="marks_student?id=34211">Игнатий Лихачев</a></td><td>Б8303а</td>
                </tr><tr>
                    <td align="right">5</td>
                    <td><a href="marks_student?id=34217">Кира Шилова</a></td><td>Б8303а</td>
                </tr><tr>
                    <td align="right">6</td>
                    <td><a href="marks_student?id=34269">Лука Назаров</a></td><td>Б8303а</td>
                </tr>
            </table>'''
        data = [
            {'id': 34211, 'name': 'Игнатий Лихачев'},
            {'id': 34217, 'name': 'Кира Шилова'},
            {'id': 34269, 'name': 'Лука Назаров'},
        ]

        self.assertEqual(student_list_parser(text), data)

    def test_student_parser(self):
        text = '''
            <table class="bordered marks">
                <tr>
                    <th>Дата</th>
                    <th>Задание</th>
                    <th>Баллы/вес</th>
                    <th>Тесты/оценки</th>
                </tr>
                <tr class="worktype">
                    <td colspan="4">Технология программирования</td>
                </tr>
                <tr>
                    <td>02.11.2015</td>
                    <td>
                        <a href="marks_view?tid=40113;sid=8884">Задание 2</a>
                    </td>
                    <td>1..10, 25%</td>
                    <td class="embedded">
                        <table class="bordered">
                            <col />
                            <col width="30px"/>
                            <col width="30px"/>
                            <tr>
                                <td>24.02.2016</td>
                                <td>7</td>
                                <td>1.9</td>
                            </tr>
                            <tr>
                                <td>10.02.2016</td>
                                <td>3</td>
                                <td>0.9</td>
                            </tr>
                            <tr>
                                <td>28.12.2015</td>
                                <td>2</td>
                                <td>0.7</td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr class="worktype">
                    <td colspan="4">Web-программирование 1</td>
                </tr>
                <tr>
                    <td>30.06.2015</td>
                    <td>
                        <a href="marks_view?tid=40270;sid=8884">Дополнительное задание 1</a>
                    </td>
                    <td>1..10, 14%</td>
                    <td class="embedded">
                    </td>
                </tr>
                <tr>
                    <td>16.06.2015</td>
                    <td>
                        <a href="marks_view?tid=38743;sid=8884">Отчёты</a>
                    </td>
                    <td>1..10, 4%</td>
                    <td class="embedded late">
                    </td>
                </tr>
                <tr>
                    <td>10.03.2015</td>
                    <td>
                        <a href="marks_view?tid=37563;sid=8884">CSS, меню</a>
                    </td>
                    <td>1..10, 4%</td>
                    <td class="embedded">
                        <table class="bordered">
                            <col />
                            <col width="30px"/>
                            <col width="30px"/>
                            <tr>
                                <td>17.03.2015</td>
                                <td>8</td>
                                <td>5.3</td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>'''
        data = [
            {'name': 'Технология программирования', 'tasks': [
                {'date': '02.11.2015', 'id': 40113, 'name': 'Задание 2', 'maxRate': 10, 'rateWeight': 25, 'marks': [
                    {'date': '24.02.2016', 'rate1': 7, 'rate2': 1.9},
                    {'date': '10.02.2016', 'rate1': 3, 'rate2': 0.9},
                    {'date': '28.12.2015', 'rate1': 2, 'rate2': 0.7},
                ]},
            ]},
            {'name': 'Web-программирование 1', 'tasks': [
                {
                    'id': 40270, 'date': '30.06.2015', 'name': 'Дополнительное задание 1', 'maxRate': 10,
                    'rateWeight': 14, 'marks': []
                },
                {'date': '16.06.2015', 'id': 38743, 'name': 'Отчёты', 'maxRate': 10, 'rateWeight': 4, 'marks': []},
                {'date': '10.03.2015', 'id': 37563, 'name': 'CSS, меню', 'maxRate': 10, 'rateWeight': 4, 'marks': [
                    {'date': '17.03.2015', 'rate1': 8.0, 'rate2': 5.3},
                ]},
            ]},
        ]

        self.assertEqual(student_parser(text), data)

    def test_student_parser_bad_cases(self):
        text = '''
            <table class="bordered marks">
                <tr class="worktype">
                    <td colspan="4">Технология программирования</td>
                </tr>
                <tr>
                    <td>02.11.2015</td>
                    <td>
                        <a href="marks_view?tid=40113;sid=8884"></a>
                    </td>
                    <td>1..10, 25%</td>
                    <td class="embedded">
                    </td>
                </tr>
                <tr>
                    <td>30.06.2015</td>
                    <td>
                        <a href="marks_view?tid=40270;sid=8884">Дополнительное задание 1</a>
                    </td>
                    <td>1..10, 14%</td>
                    <td class="embedded">
                        <table class="bordered">
                            <col />
                            <col width="30px"/>
                            <col width="30px"/>
                            <tr>
                                <td>17.03.2015</td>
                                <td>8</td>
                                <td></td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td>16.06.2015</td>
                    <td>
                        <a href="marks_view?tid=38743;sid=8884">Отчёты</a>
                    </td>
                    <td>1..10, 4%</td>
                    <td class="embedded late">
                        Тесты:
                        <table class="bordered">
                            <col width1="50%"/>
                            <col width="30px"/>
                            <tr>
                                <td>24.05.2011 13:42</td>
                                <td>
                                    <a href="quiz/quiz.xhtml?t=HdF3OLflcT9LYHd82VZ1Bik4dbxgm01CFcYwUWOh">начать</a>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>'''
        data = [
            {'name': 'Технология программирования', 'tasks': [
                {'date': '02.11.2015', 'id': 40113, 'name': '', 'maxRate': 10, 'rateWeight': 25, 'marks': []},
                {
                    'id': 40270, 'date': '30.06.2015', 'name': 'Дополнительное задание 1', 'maxRate': 10,
                    'rateWeight': 14, 'marks': [
                        {'date': '17.03.2015', 'rate1': 8.0, 'rate2': None},
                    ]
                },
                {'date': '16.06.2015', 'id': 38743, 'name': 'Отчёты', 'maxRate': 10, 'rateWeight': 4, 'marks': []},
            ]},
        ]

        self.assertEqual(student_parser(text), data)

if __name__ == '__main__':
    unittest.main()
