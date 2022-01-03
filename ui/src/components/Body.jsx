import {useState, useEffect, useCallback} from "react";
import axios from "axios";
import {Box, Form, Button, Element} from "react-bulma-components";
import IconImage from "./IconImage";
import Field from "./Field";
import ResetButton from "./ResetButton";


function Body() {
    const api_url = import.meta.env.VITE_API_URL;
    const img_api = api_url + "img";
    const fontSizeMin = 60;
    const fontSizeMax = 400;
    const fontSizeDefault = 250
    const rotateDefault = 0

    const [fonts, setFonts] = useState([]);
    const [icon, setIcon] = useState("");
    const [style, setStyle] = useState(1);
    const [textColor, setTextColor] = useState("#f0f0f0");
    const [bgColor, setBgColor] = useState("#404040");
    const [text, setText] = useState("");
    const [font, setFont] = useState(0);
    const [fontStyle, setFontStyle] = useState(2);
    const [fontSize, setFontSize] = useState(fontSizeDefault);
    const [fontRotate, setFontRotate] = useState(rotateDefault);
    const [textOffsetX, setTextOffsetX] = useState(0);
    const [textOffsetY, setTextOffsetY] = useState(0);
    const [round, setRound] = useState(30);
    const [image, setImage] = useState(null);
    const [filename, setFilename] = useState("");
    const [imageSize, setImageSize] = useState(100);
    const [imageRotate, setImageRotate] = useState(rotateDefault);
    const [imageOffsetX, setImageOffsetX] = useState(0);
    const [imageOffsetY, setImageOffsetY] = useState(0);
    const [downloadUrl, setDownloadUrl] = useState("");

    useEffect( () => {
        axios.get(api_url + "fonts")
            .then( (res) => {
                setFonts(res.data);
            });
    }, []);

    useEffect(() => {
        const data = new FormData();
        data.append("style", style);
        data.append("text_color", textColor);
        data.append("bg_color", bgColor);
        data.append("text", text);
        data.append("font", font);
        data.append("font_style", fontStyle);
        data.append("text_offset_x", textOffsetX);
        data.append("text_offset_y", textOffsetY);
        data.append("font_size", fontSize);
        data.append("font_rotate", fontRotate);
        data.append("round", round);
        data.append("image", image);
        data.append("image_size", imageSize);
        data.append("image_rotate", imageRotate);
        data.append("image_offset_x", imageOffsetX);
        data.append("image_offset_y", imageOffsetY);

        const config = {
            responseType: 'blob'
        };
        axios.post(img_api, data, config)
            .then(res => {
                URL.revokeObjectURL(icon);
                const url = URL.createObjectURL(res.data);
                setIcon(url);
                setDownloadUrl(url);
            });
    }, [style, textColor, bgColor, text, font, fontStyle, fontSize, fontRotate, textOffsetX, textOffsetY,
        round, image, imageSize, imageRotate, imageOffsetX, imageOffsetY]);

    const handleChangeImage = useCallback((e) => {
        console.log(e.target.files[0].name);
        setImage(e.target.files[0]);
        setFilename(e.target.files[0].name);
    }, []);

    const handleClearImage = useCallback(() => {
        setImage(null);
        setFilename("");
    }, []);

    const handleChangeRound = useCallback((e) => {
        setRound(e.target.value);
        setStyle(1);
    }, []);

    return (
            <Box display="flex">
                <IconImage icon={icon} url={downloadUrl}/>
                <Element ml={5}>
                    <Element>
                        <Element display="flex">
                            {/***** Text *****/}
                            <Field label="Text">
                                <Form.Textarea value={text} onChange={(e) => {
                                                setText(e.target.value)
                                            }} cols={2} rows={2}/>
                            </Field>
                            <Field label="Font" className="ml-3">
                                <Form.Select value={font}
                                             onChange={(e) => {setFont(e.target.value)}}>
                                    {fonts.map((value, index) => {
                                        return (
                                            <option value={value.idx}>{value.font}</option>
                                        );
                                    })}
                                </Form.Select>
                            </Field>
                        </Element>
                        <Element display="flex">
                            <Element>
                                {/***** Color *****/}
                                <Field label="Color">
                                    <input type="color" value={textColor} onChange={(e) => {
                                        setTextColor(e.target.value)
                                    }} />
                                </Field>
                            </Element>
                            <Element ml={5}>
                                {/***** Text Style *****/}
                                <Field label="Style">
                                    <Form.Radio name="font_style" checked={fontStyle == 0} onChange={() => {
                                        setFontStyle(0)
                                    }} value={fontStyle}>Thin</Form.Radio>
                                    <Form.Radio name="font_style" checked={fontStyle == 1} onChange={() => {
                                        setFontStyle(1)
                                    }} value={fontStyle}>Light</Form.Radio>
                                    <Form.Radio name="font_style" checked={fontStyle == 2} onChange={() => {
                                        setFontStyle(2)
                                    }} value={fontStyle}>Regular</Form.Radio>
                                    <Form.Radio name="font_style" checked={fontStyle == 3} onChange={() => {
                                        setFontStyle(3)
                                    }} value={fontStyle}>Medium</Form.Radio>
                                    <Form.Radio name="font_style" checked={fontStyle == 4} onChange={() => {
                                        setFontStyle(4)
                                    }} value={fontStyle}>Bold</Form.Radio>
                                    <Form.Radio name="font_style" checked={fontStyle == 5} onChange={() => {
                                        setFontStyle(5)
                                    }} value={fontStyle}>Black</Form.Radio>

                                </Field>
                                <Element display="flex">
                                    <Element>
                                        {/***** Text Size *****/}
                                        <Field label="Size">
                                            <input step="1" min={fontSizeMin} max={fontSizeMax}
                                                   value={fontSize} onChange={(e) => {
                                                setFontSize(e.target.value)
                                            }} type="range"/>
                                            <ResetButton onClick={() => {
                                                setFontSize(fontSizeDefault)
                                            }}/>
                                        </Field>
                                        {/***** Text Rotate *****/}
                                        <Field label="Rotate">
                                            <input step="1" min="0" max="360"
                                                   value={fontRotate} onChange={(e) => {
                                                setFontRotate(e.target.value)
                                            }} type="range"/>
                                            <ResetButton onClick={() => {
                                                setFontRotate(rotateDefault)
                                            }}/>
                                        </Field>
                                    </Element>
                                    <Element ml={3}>
                                        {/***** Text X Offset *****/}
                                        <Field label="X Offset">
                                            <input step="1" min={-100} max={100} value={textOffsetX} onChange={(e) => {
                                                setTextOffsetX(e.target.value)
                                            }} type="range"/>
                                            <ResetButton onClick={() => {
                                                setTextOffsetX(0)
                                            }}/>
                                        </Field>
                                        {/***** Text Y Offset *****/}
                                        <Field label="Y Offset">
                                            <input step="1" min={-100} max={100} value={textOffsetY}
                                                   onChange={(e) => {
                                                       setTextOffsetY(e.target.value)
                                                   }} type="range"/>
                                            <ResetButton onClick={() => {
                                                setTextOffsetY(0)
                                            }}/>
                                        </Field>
                                    </Element>
                                </Element>
                            </Element>
                        </Element>
                        <hr/>
                        {/***** Image *****/}
                        <Field label="Image">
                            <Form.InputFile onChange={handleChangeImage} filename={filename}
                                            inputProps={{accept: "image/jpeg, image/png"}}/>
                            <ResetButton onClick={handleClearImage}/>
                        </Field>
                        <Element display="flex">
                            <Element>
                                {/***** Image Size *****/}
                                <Field label="Size">
                                    <input step="5" min="30" max="200" value={imageSize} onChange={(e) => {
                                        setImageSize(e.target.value)
                                    }} type="range"/>
                                    <ResetButton onClick={() => {
                                        setImageSize(100)
                                    }}/>
                                </Field>
                                {/***** Text Rotate *****/}
                                <Field label="Rotate">
                                    <input step="1" min="0" max="360"
                                           value={imageRotate} onChange={(e) => {
                                        setImageRotate(e.target.value)
                                    }} type="range"/>
                                    <ResetButton onClick={() => {
                                        setImageRotate(rotateDefault)
                                    }}/>
                                </Field>
                            </Element>
                            <Element ml={3}>
                                {/***** Image X Offset *****/}
                                <Field label="X Offset">
                                    <input step="1" min={-100} max={100}
                                           value={imageOffsetX} onChange={(e) => {
                                        setImageOffsetX(e.target.value)
                                    }} type="range"/>
                                    <ResetButton onClick={() => {
                                        setImageOffsetX(0)
                                    }}/>
                                </Field>
                                {/***** Image Y Offset *****/}
                                <Field label="Y Offset">
                                    <input step="1" min={-100} max={100}
                                           value={imageOffsetY} onChange={(e) => {
                                        setImageOffsetY(e.target.value)
                                    }} type="range"/>
                                    <ResetButton onClick={() => {
                                        setImageOffsetY(0)
                                    }}/>
                                </Field>
                            </Element>
                        </Element>
                    </Element>
                    <hr/>
                    <Element>
                        <Form.Label>Background</Form.Label>
                        <Element display="flex">
                            {/***** Background Color *****/}
                            <Field label="Color">
                                <input type="color" value={bgColor} onChange={(e) => {
                                    setBgColor(e.target.value)
                                }}/>
                            </Field>
                            <Element ml={5}>
                                {/***** Style *****/}
                                <Field label="Style">
                                    <Form.Radio name="style" checked={style == 0} onChange={() => {
                                        setStyle(0)
                                    }} value={style}>Square</Form.Radio>
                                    <Form.Radio name="style" checked={style == 1} onChange={() => {
                                        setStyle(1)
                                    }} value={style}>Round</Form.Radio>
                                    <Form.Radio name="style" checked={style == 2} onChange={() => {
                                        setStyle(2)
                                    }} value={style}>Circle</Form.Radio>
                                </Field>
                                {/***** Round *****/}
                                <Field label="Round">
                                    <input step="5" min="30" max="90"
                                           value={round} onChange={handleChangeRound} type="range"/>
                                </Field>
                            </Element>
                        </Element>
                    </Element>
                </Element>
            </Box>
    );
}

export default Body;
