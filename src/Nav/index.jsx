import { kebabCase } from 'lodash';
import { useState } from 'react';
import { useHistory } from 'react-router-dom';

// styles
import './style.scss';

const Nav = ({categories}) => {

  const [open, setOpen] = useState(false)
  const history = useHistory();

  const close = () => setOpen(false)
  history.listen( () => open && close() );

  const handleLinkClick = (category) => {
    close()
    if (!category) return history.push(`/`);
    return history.push(`/category/${ kebabCase(category) }`);
  }

  return (
    <div id={'nav'}>
      <span id={'nav-spacer'}/>

      <nav>
        <div id={'nav-dropdown'} className={open ? 'open' : ''}>
          <div id={'category-list'}>
            <h3>Categories</h3>

            <button onClick={() => handleLinkClick()}>
              <p>All Categories</p>
            </button>

            { categories.map( (category, index) => {
              return <button key={index} onClick={() => handleLinkClick(category)}>
                <p>{ category }</p>
              </button>
            })}
          </div>
        </div>

        <div id={'static-content'}>
          <button onClick={() => setOpen(!open)} className={open ? 'open' : ''}>
            <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24" viewBox="0 0 24 24" width="24"><g><path d="M0,0h24v24H0V0z" fill="none"/></g><g><polygon points="6.23,20.23 8,22 18,12 8,2 6.23,3.77 14.46,12"/></g></svg>
          </button>
        </div>
      </nav>
    </div>
  );
}

export default Nav;
