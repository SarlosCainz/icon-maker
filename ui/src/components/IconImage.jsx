import {Columns, Block, Button} from "react-bulma-components";

function IconImage({icon, url}) {
    return (
        <Block textAlign="center" mx={3}>
            <img src={icon} alt="image" style={{width: "256px"}} />
            <Block mt={3}>
                <Button renderAs="a" color="dark" rounded={true} href={url} download="icon.png">Download</Button>
            </Block>
        </Block>
    );
}

export default IconImage