import { Link } from "react-router-dom";

// styles
import './style.scss';

// utils
import { filterCategories } from "../utils";
import { kebabCase } from 'lodash';


const ArticleCard = ({article, link, category}) => {

  const _tags = filterCategories(article.tags);

  const ArticleLink = ({children}) => (
    <Link to={link}>
      {children}
    </Link>
  )

  return (
    <div className={'article-card'}>
      
      <ArticleLink>
        <img src={article.cover_image} alt=""/>
      </ArticleLink>

      <div className={'card-info'}>
        
        <span>
          <span className={'date mono'}>{article.date}</span>
          <ArticleLink>
            <h3 className={'title'}>{ article.title }</h3>
          </ArticleLink>
          <p className={'description'}>{article.description } </p>
        </span>

        { _tags.length > 0 &&
          <div className={'tags-list'}>
            { _tags.map((tag, index) => {

              return <Link 
                key={index} 
                className={`tag mono ${category === kebabCase(tag) ? 'active' : ''}`} 
                to={`/category/${kebabCase(tag)}`}
              >{tag}</Link>
            })}
          </div> 
        }
      </div>


    </div>
  );
}

export default ArticleCard;
