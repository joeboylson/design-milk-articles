import { useEffect, useState } from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import { filterArticles } from '../utils';


// components
import Article from '../Article';
import ArticleList from '../ArticleList';
import Footer from "../Footer";

// utils

const App = () => {

  const [articles, setArticles] = useState();

  useEffect(() => {
    if (!articles) {
      fetch("/data")
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
          <Footer/>
        </Route>
        
        <Route path={[ "/articles", "/category/:category", "/" ]}>
          <ArticleList articles={articles}/>
          <Footer/>
        </Route>

      </Switch>
    </BrowserRouter>
  );
}

export default App;
