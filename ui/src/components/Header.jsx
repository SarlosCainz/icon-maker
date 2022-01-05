import "bulma/css/bulma.min.css";
import {Navbar, Heading, Image, Element} from "react-bulma-components";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faTwitterSquare, faTwitter} from "@fortawesome/free-brands-svg-icons";
import logo from "../../icon-192.png";

function Header() {
    return (
        <Navbar color="light" fixed="top">
            <Navbar.Brand>
                <Navbar.Item mx={3} href="">
                    <Image src={logo} />
                    <Heading ml={2} textColor="grey-dark">IconMaker</Heading>
                </Navbar.Item>
            </Navbar.Brand>
        </Navbar>
    );
}

export default Header;
