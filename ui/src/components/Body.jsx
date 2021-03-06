import {useState, useEffect, useCallback, useContext} from "react";
import axios from "axios";
import {Form, Button, Element} from "react-bulma-components";
import Field from "./Field";
import ResetButton from "./ResetButton";
import {values} from "../values";
import {AppContext} from "../app";


function Body() {
    const appContext = useContext(AppContext);

    const api_url = import.meta.env.VITE_API_URL;
    const img_api = api_url + "img";

    const [sendData, setSendData] = useState(null);
    const [langs, setLangs] = useState([]);
    const [icon, setIcon] = useState("");
    const [style, setStyle] = useState(values.default.style);
    const [prevStyle, setPrevStyle] = useState(values.default.style);
    const [textColor, setTextColor] = useState(values.default.textColor);
    const [bgColor, setBgColor] = useState(values.default.bgColor);
    const [text, setText] = useState(values.default.text);
    const [lang, setLang] = useState(values.default.lang);
    const [fontStyle, setFontStyle] = useState(values.default.fontStyle);
    const [fontSize, setFontSize] = useState(values.default.fontSize);
    const [fontRotate, setFontRotate] = useState(values.default.rotate);
    const [textOffsetX, setTextOffsetX] = useState(values.default.textOffsetX);
    const [textOffsetY, setTextOffsetY] = useState(values.default.textOffsetX);
    const [round, setRound] = useState(values.default.round);
    const [image, setImage] = useState(null);
    const [filename, setFilename] = useState("");
    const [imageSize, setImageSize] = useState(values.default.imageSize);
    const [imageRotate, setImageRotate] = useState(values.default.rotate);
    const [imageOffsetX, setImageOffsetX] = useState(values.default.imageOffsetX);
    const [imageOffsetY, setImageOffsetY] = useState(values.default.imageOffsetY);
    const [downloadUrl, setDownloadUrl] = useState("");
    const [forIOS, setForIOS] = useState(0);
    const [forWeb, setForWeb] = useState(0);

    useEffect(() => {
        axios.get(api_url + "lang")
            .then((res) => {
                setLangs(res.data.list);
                setLang(res.data.default);
            });
    }, []);

    useEffect(() => {
        const data = new FormData();
        data.append("style", style);
        data.append("text_color", textColor);
        data.append("bg_color", bgColor);
        data.append("text", text);
        data.append("font_style", fontStyle);
        data.append("text_offset_x", textOffsetX);
        data.append("text_offset_y", textOffsetY);
        data.append("font_size", fontSize);
        data.append("font_rotate", 360 - fontRotate - 180);
        data.append("round", round);
        data.append("image", image);
        data.append("image_size", imageSize);
        data.append("image_rotate", 360 - imageRotate - 180);
        data.append("image_offset_x", imageOffsetX);
        data.append("image_offset_y", imageOffsetY);
        data.append("lang", lang);
        setSendData(data);

        const config = {
            responseType: 'blob'
        };
        axios.post(img_api, data, config)
            .then( res => {
                if (res.status === 200) {
                    URL.revokeObjectURL(icon);
                    let url = URL.createObjectURL(res.data);
                    setIcon(url);
                }
            })
            .catch(error);
    }, [style, textColor, bgColor, text, lang, fontStyle, fontSize, fontRotate, textOffsetX, textOffsetY,
        round, image, imageSize, imageRotate, imageOffsetX, imageOffsetY]);

    useEffect( () => {
        setText(values.default.text);
        setTextColor(values.default.textColor);
        setTextOffsetX(values.default.textOffsetX);
        setTextOffsetY(values.default.textOffsetY);
        setFontSize(values.default.fontSize);
        setFontStyle(values.default.fontStyle);
        setFontRotate(values.default.rotate);
        setImage(null);
        setFilename("");
        setImageSize(values.default.imageSize);
        setImageOffsetX(values.default.imageOffsetX);
        setImageOffsetY(values.default.imageOffsetY);
        setImageRotate(values.default.rotate);
        setBgColor(values.default.bgColor);
        setStyle(values.default.style);
        setRound(values.default.round);
    }, [appContext.resetAll.value]);

    const handleChangeImage = useCallback((e) => {
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

    const handleChangeForWeb = useCallback( (e) => {
        const value = e.target.checked ? 1 : 0
        setForWeb(value)
    }, []);

    const handleChangeForIOS = useCallback( (e) => {
        const value = e.target.checked ? 1 : 0
        setForIOS(value);
        if (value === 1) {
            if (style !== 0) {
                setPrevStyle(style);
                setStyle(0);
                setForWeb(0)
            }
        } else {
            if (style !== prevStyle) {
                setStyle(prevStyle);
            }
        }
    }, [style, prevStyle]);

    const handleDownload = useCallback( () => {
        const data = sendData;
        data.append("for_ios", forIOS);
        data.append("for_web", forWeb);

        const config = {
            responseType: 'blob'
        };
        axios.post(img_api, data, config)
            .then ( res => {
                URL.revokeObjectURL(downloadUrl);
                const url = URL.createObjectURL(res.data);
                setDownloadUrl(url);

                const elm = document.createElement("a");
                elm.setAttribute("href", url)
                const filename = (forIOS || forWeb) ? "icon.zip" : "icon.png";
                elm.setAttribute("download", filename);
                elm.click();
            })
            .catch( error );
    }, [sendData, forIOS, forWeb]);

    const error = useCallback( err => {
        const status = err.response.status;
        if (status === 413) {
            alert("Client intended to send too large body.\nThe size of the image file that can be handled is up to 500KByte.");
        } else {
            alert(err.response.statusText);
        }
    }, []);

    return (
        <Element mt={3} display="flex" flexWrap="wrap">
            <Element textAlign="center" mx={3} flexGrow={1} mb={5}>
                <img src={icon} alt="image" style={{width: "256px"}}/>
                <Element mt={3}>
                    <Element display="inline-block" textAlign="left">
                        <Form.Checkbox value="1" onChange={handleChangeForIOS}>
                            for iPhone/iPad App
                        </Form.Checkbox>
                        <br />
                        <Form.Checkbox value="1" checked={forWeb === 1} disabled={forIOS === 1} onChange={handleChangeForWeb}>
                            for Web
                        </Form.Checkbox>
                    </Element>
                </Element>
                <Element mt={3}>
                    <Button renderAs="a" color="dark" rounded={true} onClick={handleDownload}>Download</Button>
                </Element>
            </Element>

            <Element ml={5} flexGrow={2}>
                <Element>
                    <Element display="flex">
                        {/***** Text *****/}
                        <Field label="Text">
                            <Form.Textarea value={text} cols={2} rows={2}
                                           onChange={(e)=>{setText(e.target.value)}} />
                        </Field>
                        <Field label="Language" className="ml-3">
                            <Form.Select value={lang}
                                         onChange={(e) => {
                                             setLang(e.target.value)
                                         }}>
                                {langs.map((value, index) => {
                                    return (
                                        <option key={index} value={value.idx}>{value.lang}</option>
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
                                }}/>
                            </Field>
                        </Element>
                        <Element ml={5}>
                            {/***** Text Style *****/}
                            <Field label="Style">
                                <Form.Radio name="font_style" checked={fontStyle === 0} onChange={() => {
                                    setFontStyle(0)
                                }} value={fontStyle}>Thin</Form.Radio>
                                <Form.Radio name="font_style" checked={fontStyle === 1} onChange={() => {
                                    setFontStyle(1)
                                }} value={fontStyle}>Light</Form.Radio>
                                <Form.Radio name="font_style" checked={fontStyle === 2} onChange={() => {
                                    setFontStyle(2)
                                }} value={fontStyle}>Regular</Form.Radio>
                                <Form.Radio name="font_style" checked={fontStyle === 3} onChange={() => {
                                    setFontStyle(3)
                                }} value={fontStyle}>Medium</Form.Radio>
                                <Form.Radio name="font_style" checked={fontStyle === 4} onChange={() => {
                                    setFontStyle(4)
                                }} value={fontStyle}>Bold</Form.Radio>
                                <Form.Radio name="font_style" checked={fontStyle === 5} onChange={() => {
                                    setFontStyle(5)
                                }} value={fontStyle}>Black</Form.Radio>

                            </Field>
                            <Element display="flex" flexWrap="wrap">
                                <Element mr={3}>
                                    {/***** Text Size *****/}
                                    <Field label="Size">
                                        <input step="1" min={values.default.fontSizeMin} max={values.default.fontSizeMax}
                                               value={fontSize} onChange={(e) => {
                                            setFontSize(e.target.value)
                                        }} type="range"/>
                                        <ResetButton onClick={() => {
                                            setFontSize(values.default.fontSize)
                                        }}/>
                                    </Field>
                                    {/***** Text Rotate *****/}
                                    <Field label="Rotate">
                                        <input step="1" min="0" max="360"
                                               value={fontRotate} onChange={(e) => {
                                            setFontRotate(e.target.value)
                                        }} type="range"/>
                                        <ResetButton onClick={() => {
                                            setFontRotate(values.default.rotate)
                                        }}/>
                                    </Field>
                                </Element>
                                <Element>
                                    {/***** Text X Offset *****/}
                                    <Field label="X Offset">
                                        <input step="1" min={-100} max={100} value={textOffsetX} onChange={(e) => {
                                            setTextOffsetX(e.target.value)
                                        }} type="range"/>
                                        <ResetButton onClick={() => {
                                            setTextOffsetX(values.default.textOffsetX)
                                        }}/>
                                    </Field>
                                    {/***** Text Y Offset *****/}
                                    <Field label="Y Offset">
                                        <input step="1" min={-100} max={100} value={textOffsetY}
                                               onChange={(e) => {
                                                   setTextOffsetY(e.target.value)
                                               }} type="range"/>
                                        <ResetButton onClick={() => {
                                            setTextOffsetY(values.default.textOffsetY)
                                        }}/>
                                    </Field>
                                </Element>
                            </Element>
                        </Element>
                    </Element>
                    <hr/>
                    {/***** Image *****/}
                    <Field label="Image" note="* The file size is up to 500KByte.">
                        <Form.InputFile onChange={handleChangeImage} filename={filename}
                                        inputProps={{accept: "image/jpeg, image/png"}}/>
                        <ResetButton onClick={handleClearImage}/>
                    </Field>
                    <Element display="flex" flexWrap="wrap">
                        <Element mr={3}>
                            {/***** Image Size *****/}
                            <Field label="Size">
                                <input step="5" min="30" max="200" value={imageSize} onChange={(e) => {
                                    setImageSize(e.target.value)
                                }} type="range"/>
                                <ResetButton onClick={() => {
                                    setImageSize(values.default.imageSize)
                                }}/>
                            </Field>
                            {/***** Text Rotate *****/}
                            <Field label="Rotate">
                                <input step="1" min="0" max="360"
                                       value={imageRotate} onChange={(e) => {
                                    setImageRotate(e.target.value)
                                }} type="range"/>
                                <ResetButton onClick={() => {
                                    setImageRotate(values.default.rotate)
                                }}/>
                            </Field>
                        </Element>
                        <Element>
                            {/***** Image X Offset *****/}
                            <Field label="X Offset">
                                <input step="1" min={-100} max={100}
                                       value={imageOffsetX} onChange={(e) => {
                                    setImageOffsetX(e.target.value)
                                }} type="range"/>
                                <ResetButton onClick={() => {
                                    setImageOffsetX(values.default.imageOffsetX)
                                }}/>
                            </Field>
                            {/***** Image Y Offset *****/}
                            <Field label="Y Offset">
                                <input step="1" min={-100} max={100}
                                       value={imageOffsetY} onChange={(e) => {
                                    setImageOffsetY(e.target.value)
                                }} type="range"/>
                                <ResetButton onClick={() => {
                                    setImageOffsetY(values.default.imageOffsetY)
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
                                <Form.Radio name="style" checked={style === 0} onChange={() => {
                                    setStyle(0)
                                }} value={style} disabled={forIOS === 1}>Square</Form.Radio>
                                <Form.Radio name="style" checked={style === 1} onChange={() => {
                                    setStyle(1)
                                }} value={style} disabled={forIOS === 1}>Round</Form.Radio>
                                <Form.Radio name="style" checked={style === 2} onChange={() => {
                                    setStyle(2)
                                }} value={style} disabled={forIOS === 1}>Circle</Form.Radio>
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
        </Element>
    );
}

export default Body;
