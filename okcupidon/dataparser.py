from bs4 import BeautifulSoup


def parse_profile(profile_id, html_page):
    """This function parses the html page, looking for profile data and returns a dict """
    
    soup = BeautifulSoup(html_page, "html.parser")
    data_structure = {
        'age': ['span', {'class': 'profile-basics-asl-age'}],
        'location': ['span', {'class': 'profile-basics-asl-location'}],
        'essays': {'category': ['h2', {'class': 'profile-essay-category'}],
                   'title': ['h2', {'class': 'profile-essay-title'}],
                   'contents': ['p', {'class': 'profile-essay-contents'}]
                   },
        'details': {'basic': ['div', {
                        'class': 'matchprofile-details-section matchprofile-details-section--basics'}],
                    'badge': ['div', {
                        'class': 'matchprofile-details-section matchprofile-details-section--black-lives-matter'}],
                    'pronoun': ['div', {
                        'class': 'matchprofile-details-section matchprofile-details-section--pronouns'}],
                    'looks': ['div', {
                        'class': 'matchprofile-details-section matchprofile-details-section--looks'}],
                    'background': ['div', {
                        'class': 'matchprofile-details-section matchprofile-details-section--background'}],
                    'lifestyle': ['div', {
                        'class': 'matchprofile-details-section matchprofile-details-section--lifestyle'}],
                    'family': ['div', {
                        'class': 'matchprofile-details-section matchprofile-details-section--family'}],
                    'wiw': ['div', {
                        'class': 'matchprofile-details-section matchprofile-details-section--wiw'}],
                    }
    }
    parsed_data = {}

    # Basic info - id
    parsed_data['id'] = profile_id

    # Basic info - age
    parsed_data['age'] = soup.find_all(
        data_structure.get('age')[0],
        data_structure.get('age')[1])[0].text

    # Basic info - location
    parsed_data['location'] = soup.find_all(
        data_structure.get('location')[0],
        data_structure.get('location')[1])[0].text

    # Essays
    parsed_data['essays'] = list()
    for box in soup.find_all('div', {'class': 'profile-essay'}):
        box_essay = {}
        box_essay['category'] = box.find_all(
            data_structure['essays'].get('category')[0],
            data_structure['essays'].get('category')[1])[0].text

        box_essay['title'] = box.find_all(
            data_structure['essays'].get('title')[0],
            data_structure['essays'].get('title')[1])[0].text

        box_essay['contents'] = box.find_all(
            data_structure['essays'].get('contents')[0],
            data_structure['essays'].get('contents')[1])[0].text

        parsed_data['essays'].append(box_essay)

    # Details column
    parsed_data['details'] = {}
    for section in soup.find_all('div', {'class': 'quickmatch-profiledetails matchprofile-details'}):
        for detail in data_structure['details'].keys():

            element = data_structure['details'][detail][0]
            css_class = data_structure['details'][detail][1]['class']

            if section.find(element, css_class):
                parsed_data['details'][detail] = section.find(element, css_class).\
                find('div', 'matchprofile-details-text').text

    return parsed_data
