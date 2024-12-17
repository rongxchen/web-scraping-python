from bs4 import BeautifulSoup


def process_douban_250_one_page(html_str: str):
    html = BeautifulSoup(html_str, "html.parser")
    items = html.select(".item")
    res = []
    for item in items:
        try:
            movie_url = item.select_one(".pic a")["href"]
            img_url = item.select_one(".pic img")["src"]
            info = item.select_one(".info")
            title = "".join(span.text.strip() for span in info.select_one(".hd a").select("span"))
            title = title.replace("\xa0", "").replace(" ", "")
            rating = float(info.select_one(".bd .rating_num").text)
            comment_count = int(info.select_one(".star").select("span")[-1].text.replace("人评价", ""))
            quote = info.select_one(".bd .quote")
            introduction = quote.select_one(".inq").text.strip() if quote is not None else ""
            info2 = info.select_one(".bd").select("p")[0].text.strip().split("\n")
            persons = info2[0].split("\xa0\xa0\xa0")
            if len(persons) == 2:
                directors, performers = persons
            else:
                directors = persons[0]
            descriptions = info2[1].strip().replace("\xa0", "").split("/")
            if len(descriptions) == 3:
                year, location, categories = descriptions
            elif len(descriptions) == 4:
                year, location, categories = " ".join(descriptions[:2]), descriptions[2], descriptions[3]
            else:
                year, location, categories = "", "", ""
            res.append({
                "movie_url": movie_url,
                "img_url": img_url,
                "title": title,
                "rating": rating,
                "comment_count": comment_count,
                "introduction": introduction,
                "directors": directors.replace("导演: ", ""),
                "performers": performers.replace("主演: ", ""),
                "year": year,
                "location": location,
                "categories": categories
            })
        except Exception as e:
            print("".join(span.text.strip() for span in info.select_one(".hd a").select("span")))
            print(e)
    return res
