import "bulma/css/bulma.min.css";
import {Navbar, Heading, Element} from "react-bulma-components";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTwitterSquare, faTwitter} from "@fortawesome/free-brands-svg-icons";
import logo from "../../logo.png";

function Header() {
    return (
        <Navbar color="light">
            <Navbar.Brand>
                <Navbar.Item mx={3}>
                    <img src={logo} />
                    <Heading ml={2} textColor="grey-dark">IconMaker</Heading>
                </Navbar.Item>
            </Navbar.Brand>
            <Navbar.Menu>
                <Navbar.Container align="right">
                    <Navbar.Item href="https://twitter.com/sarlos_cainz">
                        <FontAwesomeIcon icon={faTwitterSquare} size="2x" color="#1DA1F2" />
                    </Navbar.Item>
                </Navbar.Container>
            </Navbar.Menu>
        </Navbar>
    );
}

export default Header;
