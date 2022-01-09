import {useContext} from "react";
import {Navbar, Heading, Image} from "react-bulma-components";
import logo from "../../icon-192.png";
import {AppContext} from "../app";

function Header() {
    const appContext = useContext(AppContext);

    return (
        <Navbar color="light" fixed="top" active={appContext.burgerMenu.value}>
            <Navbar.Brand>
                <Navbar.Item mx={3}>
                    <img src={logo} alt="M"/>
                    <Heading ml={2} textColor="grey-dark">IconMaker</Heading>
                </Navbar.Item>
                <Navbar.Burger onClick={appContext.burgerMenu.toggle} />
            </Navbar.Brand>
            <Navbar.Menu>
                <Navbar.Container align="left">
                    <Navbar.Item onClick={appContext.resetAll.do}>
                        <Navbar.Link arrowless={true}>ResetAll</Navbar.Link>
                    </Navbar.Item>
                </Navbar.Container>
            </Navbar.Menu>
        </Navbar>
    );
}

export default Header;
