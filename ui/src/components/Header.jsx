import "bulma/css/bulma.min.css";
import {Navbar, Heading} from "react-bulma-components";
import logo from "../../logo.png";

function Header() {
    return (
        <Navbar color="light">
            <Navbar.Brand>
                <Navbar.Item mx={3}>
                    <img src={logo} className="mt-1"/>
                    <Heading ml={2} textColor="grey-dark">IconMaker</Heading>
                </Navbar.Item>
            </Navbar.Brand>
        </Navbar>
    );
}

export default Header;
