import React from 'react';
import Giscus from "@giscus/react";
import { useColorMode } from '@docusaurus/theme-common';

export default function GiscusComponent() {
  const { colorMode } = useColorMode();

  return (
    <div style={{marginTop: '20px'}}>
      <Giscus
        repo="TakeaimK/TakeaimK.github.io"
        repoId="R_kgDOQ3D12A"
        category="General"
        categoryId="DIC_kwDOQ3D12M4C2oKj"
        mapping="pathname"
        strict="0"
        reactionsEnabled="1"
        emitMetadata="0"
        inputPosition="bottom"
        theme={colorMode}
        lang="ko"
        loading="lazy"
        crossorigin="anonymous"
        async
      />
    </div>
  );
}
