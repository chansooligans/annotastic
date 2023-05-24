
import { annotate, annotationGroup } from 'https://unpkg.com/rough-notation?module';

const e0 = document.querySelector('span#revision0');
const e1 = document.querySelector('span#revision1');
const e2 = document.querySelector('span#revision2');
const e3 = document.querySelector('span#revision3');
const e5 = document.querySelector('span#revision5');
const e6 = document.querySelector('span#revision6');
const e7 = document.querySelector('span#revision7');
const e8 = document.querySelector('span#revision8');
const e9 = document.querySelector('span#revision9');
const e11 = document.querySelector('span#revision11');
const e12 = document.querySelector('span#revision12');
const e13 = document.querySelector('span#revision13');
const e14 = document.querySelector('span#revision14');

const a0 = annotate(e0, { type: 'underline', color: 'orange' });
const a1 = annotate(e1, { type: 'underline', color: 'orange' });
const a2 = annotate(e2, { type: 'box', color: 'grey' });
const a3 = annotate(e3, { type: 'underline', color: 'orange' });
const a5 = annotate(e5, { type: 'underline', color: 'grey' });
const a6 = annotate(e6, { type: 'box', color: 'grey' });
const a7 = annotate(e7, { type: 'circle', color: 'grey' });
const a8 = annotate(e8, { type: 'box', color: 'orange' });
const a9 = annotate(e9, { type: 'underline', color: 'orange' });
const a11 = annotate(e11, { type: 'box', color: 'grey' });
const a12 = annotate(e12, { type: 'underline', color: 'grey' });
const a13 = annotate(e13, { type: 'bracket', color: 'orange' });
const a14 = annotate(e14, { type: 'underline', color: 'orange' });

const animation = annotationGroup([a0, a1, a2, a3, a5, a6, a7, a8, a9, a11, a12, a13, a14]);
animation.show();
