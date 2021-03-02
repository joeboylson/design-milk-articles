import { useEffect } from "react";
import { useHistory, useParams } from "react-router-dom";

import "./style.scss";

const Article = ({articles}) => {

  const { articleId } = useParams();
  const { goBack } = useHistory();

  const article = articles.find(a => a.id === articleId);

  useEffect(() => {
    window.scrollTo(0, 0)
  })

  const _html = article.body_raw.replaceAll('loading="lazy"', "")

  return (
    <div className={'article'}>

      <button onClick={goBack} className={'back-button'}>
        <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
          <path d="M0 0h24v24H0z" fill="none"/>
          <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
        </svg>
      </button>

      <div className={'article-content'}>
        <div className={'article-header'}>
          <h2>{article.title}</h2>
        </div>

        <div className={'article-info'}>
          <div className={'article-info-image'}>
            <img src={article.cover_image} alt={'article cover'}/>
          </div>

          <div className={'article-info-text'}>
            <p className={'description mono small'}>{article.description}</p>
            <p>\\\</p>
            <p className={'date mono small'}>{article.date}</p>
            <p>\\\</p>
            <p className={'reference mono small'}>Article By: <a href={article.posted_by_label.href} target={'__blank'}>{article.posted_by_label.name}</a></p>
          </div>
        </div>

        {/* 
          I don't like my use of "dangerouslySetInnerHTML" . . .
          however, I am lazy and to do it the right way would take be a lot of work.
        */}
        <div className={'article-body'} dangerouslySetInnerHTML={{ __html: _html }}></div>
      </div>

    </div>
  );
}

export default Article;
