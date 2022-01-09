import {Element, Navbar} from "react-bulma-components";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTwitterSquare, faGithub} from "@fortawesome/free-brands-svg-icons";

function Footer() {
    return (
        <>
            <Element display="flex" justifyContent="right" my={5}>
                <Element renderAs="a" display="flex" alignItems="center" mx={3}
                         href="https://twitter.com/sarlos_cainz">
                    <FontAwesomeIcon icon={faTwitterSquare} color="#aaa"/>
                    <Element ml={1} textSize={7}>@SarlosCainz</Element>
                </Element>
                <Element renderAs="a" display="flex" alignItems="center" mr={4}
                         href="https://github.com/SarlosCainz/icon-maker">
                    <FontAwesomeIcon icon={faGithub} color="#aaa"/>
                    <Element ml={1} textSize={7}>SarlosCainz</Element>
                </Element>
            </Element>
        </>
    );
}

export default Footer;
