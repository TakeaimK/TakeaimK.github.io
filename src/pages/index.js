import React from 'react';
import  { Redirect } from '@docusaurus/router';

export default function Home() {
  // 접속하자마자 /blog 페이지로 이동시킵니다.
  return <Redirect to="/blog" />;
}