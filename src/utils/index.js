import { take, kebabCase, uniqBy, pull } from 'lodash';

export const filterArticles = (_articles) => {

  _articles = uniqBy(_articles, a => kebabCase(a.title) );

  _articles = _articles.filter(a => {
    if (!a.cover_image) return false;
    if (a.cover_image.includes('shopify')) return false;
    return a;
  })

  return _articles;
};

export const filterCategories = (_categories) => {
  _categories = pull(_categories, 'Main');
  _categories = pull(_categories, 'Sponsor');
  return _categories
}

export const getArticlesByCategory = (_articles, _category) => {
  if (!_category) return _articles;
  return _articles.filter(a => {
    const slugified_tags = a.tags.map(t => kebabCase(t));
    return slugified_tags.includes(_category)
  });
}