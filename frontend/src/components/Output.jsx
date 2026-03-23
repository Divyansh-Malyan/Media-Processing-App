function Output({ result, operation }) {

    if (!result) return null;

    if (operation === "thumbnail") {
        return (
            <>
                <img src={result} width="100%"/>
            </>
        );
    }

    if (operation === "compress") {
        return (
            <>
                <video controls width="100%">
                    <source src={result} type="video/mp4" />
                </video>
            </>
        );
    }

    if (operation === "extract_audio") {
        return (
            <>
                <audio controls style={{ width: "100%" }}>
                    <source src={result} type="audio/mpeg" />
                </audio>
            </>
        );
    }

    return null;
}

export default Output;
