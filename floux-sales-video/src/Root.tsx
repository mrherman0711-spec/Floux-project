import "./index.css";
import { Composition } from "remotion";
import { FlouxSalesVideo } from "./FlouxSalesVideo";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="FlouxSalesEmail"
        component={FlouxSalesVideo}
        durationInFrames={1260}
        fps={30}
        width={1280}
        height={720}
      />
    </>
  );
};
