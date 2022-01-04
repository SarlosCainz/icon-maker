import {Element, Button} from "react-bulma-components";

function IconImage({icon, url}) {
    return (
        <Element textAlign="center" mx={3} flexGrow={1} mb={5}>
            <img src={icon} alt="image" style={{width: "256px"}} />
            <Element mt={3}>
                <Button renderAs="a" color="dark" rounded={true} href={url} download="icon.png">Download</Button>
            </Element>
        </Element>
    );
}

export default IconImage