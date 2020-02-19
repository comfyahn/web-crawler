from bs4 import BeautifulSoup
import requests
import re

class MovieService():

    def current_running_movie_get(self):
        raw = requests.get("https://movie.naver.com/movie/running/current.nhn")

        html = BeautifulSoup(raw.text, 'html.parser')
        movies = html.select("ul.lst_detail_t1 li")
        response = []

        for i, m in enumerate(movies):

            if i > 30:
                break

            result = {}

            # 썸네일
            thumb = m.select_one("div.thumb a img").get('src')
            # print(thumb)
            result['thumb'] = thumb

            # 영화코드
            code = m.select_one("div.thumb a").get('href')
            # print(code)
            result['code'] = code.split('code=')[1]

            # 등급
            grade = m.select_one("dt.tit span")
            if grade is not None:
                # print(grade)
                result['grade'] = grade.text

            # 제목
            title = m.select_one("dt.tit a").text
            # print(title)
            result['title'] = title

            # 평점
            score = m.select_one("dl.info_star div.star_t1 span.num").text
            # print(score)
            result['score'] = score

            # 예매율
            # 예매율이 없는 경우가 있음
            rate = m.select_one("dl.info_exp div.star_t1 span.num")
            if rate is not None:
                # print(rate)
                result['rate'] = rate.text

            # 개요
            genre = m.select("dl.info_txt1 dd:nth-of-type(1) .link_txt a")
            genre_list = []
            for g in genre:
                # print(g.text)
                genre_list.append(g.text)
            result['genre'] = genre_list

            # 상영 시간은 단순 텍스트라 앞뒤 태그 제거 후 사용
            info_txt = m.select("dl.info_txt1 dd:nth-of-type(1)")[0]
            span = info_txt.select('span')
            for extract_tag in span:
                extract_tag.extract()

            split_info_txt = info_txt.getText().split("분")

            showTm = split_info_txt[0].strip()
            # print(showTm)
            result['showTm'] = showTm

            openDt = split_info_txt[1].strip()
            # print(openDt)
            result['openDt'] = openDt

            # 감독
            director = m.select("dl.info_txt1 dd:nth-of-type(2) .link_txt a")
            director_list = []
            for d in director:
                # print(d.text)
                director_list.append(d.text)
            result['director'] = director_list

            # 배우
            actor = m.select("dl.info_txt1 dd:nth-of-type(3) .link_txt a")
            actor_list = []
            for a in actor:
                # print(a.text)
                actor_list.append(a.text)
            result['actor'] = actor_list

            # # 평점이 8.5이상이면서 장르가 액션인 영화만을 고른다.
            # if float(score) < 8.5:
            #     continue

            # genre_all = m.select_one("dl.lst_dsc dl.info_txt1 dd:nth-of-type(1) span.link_txt")
            # if "액션" not in genre_all.text:    # genre_all은 태그데이터 안에서 선택했기에 .text로 바꿔주어야 한다.
            #     continue


            # print(result)
            response.append(result)
            print(response)

        return response

    def premovie_get(self):
        raw = requests.get("https://movie.naver.com/movie/running/premovie.nhn")

        html = BeautifulSoup(raw.text, 'html.parser')
        pre_movies = html.select("div.lst_wrap")
        response = []

        for pm in pre_movies:
            
            result = {}

            date_html = pm.select("div.day_t1 span span.blind")
            date = ""
            for d in date_html:
                date += d.text

            result["date"] = date
            
            result["movie"] = []            
            movies = pm.select("ul.lst_detail_t1 li")
            
            for m in movies:

                movie = {}

                thumb = m.select_one("div.thumb a img").get('src')
                movie["thumb"] = thumb

                code = m.select_one("div.thumb a").get('href')
                movie['code'] = code.split('code=')[1]

                grade = m.select_one("dl.lst_dsc dt.tit span")
                if grade is not None:
                    movie['grade'] = grade.text
                
                title = m.select_one("dl.lst_dsc dt.tit a").text
                movie["title"] = title

                exp_up = m.select_one("dl.lst_dsc dd.star dl.info_exp div.star_t1 em.exp_cnt:nth-of-type(1)")
                if exp_up is not None:
                    movie['exp_up'] = exp_up.text
                exp_down = m.select_one("dl.lst_dsc dd.star dl.info_exp div.star_t1 em.exp_cnt:nth-of-type(2)")
                if exp_down is not None:
                    movie['exp_down'] = exp_down.text

                genre = m.select("dl.lst_dsc dl.info_txt1 dd:nth-of-type(1) .link_txt a")
                genre_list = []
                for g in genre:
                    genre_list.append(g.text)
                movie['genre'] = genre_list

                director = m.select("dl.lst_dsc dl.info_txt1 dd:nth-of-type(2) .link_txt a")
                director_list = []
                for d in director:
                    director_list.append(d.text)
                movie['director'] = director_list

                actor = m.select("dl.lst_dsc dl.info_txt1 dd:nth-of-type(3) .link_txt a")
                actor_list = []
                for a in actor:
                    actor_list.append(a.text)
                movie['actor'] = actor_list

                result['movie'].append(movie)

            response.append(result)

        return response

    def story_get(self, code):
        url = "https://movie.naver.com/movie/bi/mi/basic.nhn"
        raw = requests.get(url, { 'code': code })

        html = BeautifulSoup(raw.text, 'html.parser')
        story = html.select_one("div.story_area")
        response = {}

        if story is None: return response

        print(story)

        main_summary = story.select_one(".h_tx_story")
        if main_summary is not None:
            # print(main_summary)
            response['main_summary'] = main_summary.text

        summary = story.select_one(".con_tx")
        if summary is not None:
            # print(summary)
            response['summary'] = summary.text

        return response

    def actor_get(self, code):
        url = "https://movie.naver.com/movie/bi/mi/detail.nhn"
        raw = requests.get(url, { 'code': code })

        html = BeautifulSoup(raw.text, 'html.parser')
        actor = html.select("ul.lst_people li")
        response = []

        for a in actor:
            result = {}

            thumb = a.select_one(".p_thumb a img")

            if thumb is None: continue

            # print(thumb.get("src"))
            result['thumb'] = thumb.get("src")

            name = a.select_one(".p_info a.k_name").text
            # print(name.text)
            result['name'] = name

            role = a.select_one(".p_info .p_part").text
            result['role'] = role

            product = a.select("ul.mv_product li")
            result['product'] = []

            for p in product:
                p_name = p.select_one('a').text
                p_dt = p.select_one('span').text

                result['product'].append({
                    'name': p_name,
                    'date': p_dt
                })

            response.append(result)

        return response

    def director_get(self, code):
        url = "https://movie.naver.com/movie/bi/mi/detail.nhn"
        raw = requests.get(url, { 'code': code })

        html = BeautifulSoup(raw.text, 'html.parser')
        director = html.select(".director .dir_obj")
        response = []

        for d in director:
            result = {}

            thumb = d.select_one(".thumb_dir a img").get("src")
            # print(thumb)
            result['thumb'] = thumb

            name = d.select_one(".dir_product a").text
            # print(name)
            result['name'] = name

            e_name = d.select_one(".dir_product .e_name").text
            if e_name != "":
                # print(e_name)
                result['e_name'] = e_name

            response.append(result)

        return response

    def photo_last_paging_number_get(self, code):
        url = "https://movie.naver.com/movie/bi/mi/photo.nhn"
        raw = requests.get(url, { 'code': code })

        html = BeautifulSoup(raw.text, 'html.parser')
        paging = html.select("div.paging div a span")
        response = {}

        if len(paging) == 0:
            response["last_paging"] = 1
        else:
            for last_paging in paging:pass
            if last_paging:
                response["last_paging"] = int(last_paging.text)

        return response

    def photo_get(self, code, page):
        url = "https://movie.naver.com/movie/bi/mi/photo.nhn"
        photo_raw = requests.get(url, { 'code': code, 'page': page })
        photo_html = BeautifulSoup(photo_raw.text, 'html.parser')
        photos = photo_html.select(".photo .gallery_group ul li")
        response = []

        for photo in photos:
            image = photo.select_one("a img").get("src")
            response.append(image)

        return response

    def video_trailer_get(self, code):
        url = "https://movie.naver.com/movie/bi/mi/media.nhn"
        raw = requests.get(url, { 'code': code })

        html = BeautifulSoup(raw.text, 'html.parser')
        trailer = html.select("div.ifr_trailer ul.video_thumb li")
        response = []

        for t in trailer:
            result = {}

            link = t.select_one("a").get("href")
            print(link)
            result['link'] = link

            thumb = t.select_one("a img").get("src")
            print(thumb)
            result['thumb'] = thumb

            title = t.select_one("p.tx_video a").text
            print(title)
            result['title'] = title

            date = t.select_one("p.video_date").text
            print(date)
            result['date'] = date

            response.append(result)

        return response

    def video_making_get(self, code):
        url = "https://movie.naver.com/movie/bi/mi/media.nhn"
        raw = requests.get(url, { 'code': code })

        html = BeautifulSoup(raw.text, 'html.parser')
        making = html.select("div.ifr_making ul.video_thumb li")
        response = []

        for m in making:
            result = {}

            link = m.select_one("a").get("href")
            print(link)
            result['link'] = link

            thumb = m.select_one("a img").get("src")
            print(thumb)
            result['thumb'] = thumb

            title = m.select_one("p.tx_video a").text
            print(title)
            result['title'] = title

            date = m.select_one("p.video_date").text
            print(date)
            result['date'] = date

            response.append(result)

        return response

    def video_talk_get(self, code):
        url = "https://movie.naver.com/movie/bi/mi/media.nhn"
        raw = requests.get(url, { 'code': code })

        html = BeautifulSoup(raw.text, 'html.parser')
        movie_talk = html.select("div.ifr_movie_talk ul.video_thumb li")
        response = []

        for m in movie_talk:
            result = {}

            link = m.select_one("a").get("href")
            print(link)
            result['link'] = link

            thumb = m.select_one("a img").get("src")
            print(thumb)
            result['thumb'] = thumb

            title = m.select_one("p.tx_video a").text
            print(title)
            result['title'] = title

            date = m.select_one("p.video_date").text
            print(date)
            result['date'] = date

            response.append(result)

        return response

    def video_link_get(self, code, media):
        url = "https://movie.naver.com/movie/bi/mi/mediaView.nhn"
        raw = requests.get(url, { 'code': code, 'mid': media })

        html = BeautifulSoup(raw.text, 'html.parser')
        video = html.select_one("div#jPlayerArea ._videoPlayer")
        response = {}

        if video is not None:
            # print(media) 
            response['link'] = video.get("src")

        return response
        