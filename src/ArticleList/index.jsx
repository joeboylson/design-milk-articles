import { useParams, Link } from "react-router-dom";
import ArticleCard from '../ArticleCard';
import { getArticlesByCategory, filterCategories } from '../utils';
import { map, uniq, slice, take, chunk, range, kebabCase } from 'lodash';
import './style.scss';

const ArticleList = ({articles}) => {

  const getQueryVariable = (variable) => {
    var query = window.location.search.substring(1);
    var vars = query.split('&');
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split('=');
        if (decodeURIComponent(pair[0]) === variable.toString()) {
            return decodeURIComponent(pair[1]);
        }
    }
  }

  const page = Number(getQueryVariable('page')) || 1;
  const categories = filterCategories( uniq(map(articles, 'tags').flat()) )

  const { category } = useParams();
  const articlesByCategory = getArticlesByCategory(articles, category);
  const paginationLength = chunk(articlesByCategory, 30).length;
  const _articles = take( slice( articlesByCategory, (page-1) * 30), 30);

  const Pagination = () => (
    <div className={'pagination'}>
      { range(paginationLength).map(i => {
        const to = `${category ? `/category/${category}` : 'articles'}?page=${i+1}`
        const className = (i+1) === page ? 'active' : ''
        return <Link 
          key={i}
          to={to} 
          className={className}
          onClick={() => window.scrollTo(0, 0)}
        > {i+1} </Link>
      }) }
    </div>
  )
  
  return (
    <div id={'article-list'}>

      <div className={'pagination'}>
       <Link to={`/`} className={!category ? 'active' : ''}>All Categories</Link>
        { categories.map((c, index) => {
          const to = `${c ? `/category/${kebabCase(c)}` : 'articles'}?page=1`
          const className = kebabCase(c) === category ? 'active' : ''
          return <Link key={index} to={to} className={className}> {c} </Link>
        }) }
      </div>

      <Pagination/>

      { _articles.map( (article, index) => {
        return <ArticleCard 
          key={index}
          article={article} 
          link={`/article/${article.id}`}
          category={category}
        />;
      })}

      <Pagination/>

    </div>
  );
}

export default ArticleList;
