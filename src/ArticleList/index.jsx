import { useParams, Link } from "react-router-dom";
import ArticleCard from '../ArticleCard';
import { getArticlesByCategory, filterCategories } from '../utils';
import { map, uniq, slice, take, chunk, range, kebabCase } from 'lodash';
import './style.scss';

const ArticleList = ({articles}) => {

  function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) == variable) {
            return decodeURIComponent(pair[1]);
        }
    }
    console.log('Query variable %s not found', variable);
  }

  const page = Number(getQueryVariable('page')) || 1;
  const categories = filterCategories( uniq(map(articles, 'tags').flat()) )

  const { category } = useParams();
  const articlesByCategory = getArticlesByCategory(articles, category);
  const paginationLength = chunk(articlesByCategory, 30).length;
  const _articles = take( slice( articlesByCategory, (page-1) * 30), 30);
  
  return (
    <div id={'article-list'}>

      <div className={'pagination'}>
        { categories.map(c => {
          const to = `${category ? `/category/${kebabCase(c)}` : 'articles'}?page=${1}`
          const className = kebabCase(c) === category ? 'active' : ''
          return <Link to={to} className={className}> {c} </Link>
        }) }
      </div>

      <div className={'pagination'}>
        { range(paginationLength).map(i => {
          const to = `${category ? `/category/${category}` : 'articles'}?page=${i+1}`
          const className = (i+1) === page ? 'active' : ''
          return <Link to={to} className={className}> {i+1} </Link>
        }) }
      </div>

      { _articles.map( (article, index) => {
        return <ArticleCard 
          lay={index}
          article={article} 
          link={`/article/${article.id}`}
          category={category}
        />;
      })}
    </div>
  );
}

export default ArticleList;
