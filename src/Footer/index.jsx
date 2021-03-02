import './style.scss';

const Footer = () => {
  return (
    <footer>

        <div id={'footer-inner'}>
            <div>
                <h2>Legal</h2>
                <p>Photo copyright is retained by the owners of the photos.</p>
                <p>All other content is a product of and copwrited by <a href={'https://design-milk.com/'}>Design Milk</a></p>
            </div>

            <div>
                <h2>Data</h2>
                <p>Data gathered is only what is open and available for public use on <a href={'https://design-milk.com/'}>Design Milk</a></p>
                <p>Images, titles, and article content have not been changed or altered, except in the way it is displayed.</p>
                <p><a href={'/data/articles.json'} download>Download Data</a></p>
            </div>

            <div>
                <h2>Contact</h2>
                <p> <a href={'mailto:joeboylson@gmail.com'}>Contact the Developer</a> </p>
                <p> <a href={'https://github.com/joeboylson/design-milk-articles'}>Github Repository</a> </p>
            </div>
        </div>


    </footer>
  );
}

export default Footer;
