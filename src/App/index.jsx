import { useEffect, useState } from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import { filterArticles } from '../utils';


// components
import Article from '../Article';
import ArticleList from '../ArticleList';

// utils

const App = () => {

  const [articles, setArticles] = useState();

  useEffect(() => {
    if (!articles) {
      fetch("/data/articles.json")
        .then(response => response.json())
        .then(json => setArticles( filterArticles(json)))
    }
  }, [articles]);

  if (!articles) return <div></div>;

  return (
    <BrowserRouter>
      <Switch>
        <Route path="/article/:articleId">
          <Article articles={articles}/>
        </Route>
        
        <Route path={[ "/articles", "/category/:category", "/" ]}>
          <ArticleList articles={articles}/>
        </Route>

      </Switch>
    </BrowserRouter>
  );
}

export default App;
