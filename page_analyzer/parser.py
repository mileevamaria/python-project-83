from bs4 import BeautifulSoup


def parse(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    result = {}

    # h1
    h1_tag = soup.find('h1')
    result['h1'] = h1_tag.get_text(strip=True) if h1_tag else None

    # title
    title_tag = soup.find('title')
    result['title'] = title_tag.get_text(strip=True) if title_tag else None

    # meta description
    description_tag = soup.find('meta', attrs={'name': 'description'})
    result['description'] = (
        description_tag.get('content').strip()
        if description_tag and description_tag.get('content')
        else None
    )
    return result
