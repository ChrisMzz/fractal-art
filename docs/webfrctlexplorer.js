"use strict";

function main() {
  // Get A WebGL context
  /** @type {HTMLCanvasElement} */
  const canvas = document.querySelector("#canvas");
  const gl = canvas.getContext("webgl2");
  if (!gl) {
    return;
  }

  const funcs = [
    `
    for (int i=0; i<iter; i++) {

        // z**2 + c
        z = vec2(
        pow(z.x,2.0) - pow(z.y,2.0) + c.x,
        2.0*z.x*z.y + c.y
        );
        //

          `,
    `
    float p0 = `+ String(Math.random()) + `*sin(iTime*0.02+`+ String(Math.random()*4) + `);

    float anim0 = (1.) - (1.*p0*0.);
    float anim1 = (1.*p0*1.);
    
    for (int i=0; i<iter; i++) {

        z = 0.  + anim0 * vec2(
            -0.44625198674289 + ((0.7110795021893348)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(-0.28057759111876823)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.028828153683191582)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(0.584098742288947)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((0.04538315264361348)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))-(0.3585773388953144)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))),
            -0.3200820997860103 + ((-0.28057759111876823)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.7110795021893348)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.584098742288947)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.028828153683191582)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((0.3585773388953144)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))+(0.04538315264361348)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.)))
        ) + anim1 * vec2(
            -0.5584326286594536 + ((0.7819369249120012)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.5598762616238071)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.4308687379318359)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(0.4291450987864669)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((-0.26885359216242244)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))-(0.25932160814024585)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))),
            -0.39332358239423204 + ((0.5598762616238071)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.7819369249120012)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.4291450987864669)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.4308687379318359)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((0.25932160814024585)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))+(-0.26885359216242244)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.)))
        );
        `,
    `
    float p0 = `+ String(Math.random()) + `*sin(iTime*0.02+`+ String(Math.random()*4) + `);
    float p1 = `+ String(Math.random()) + `*sin(iTime*0.02+`+ String(Math.random()*4) + `);
    float p2 = `+ String(Math.random()) + `*sin(iTime*0.02+`+ String(Math.random()*4) + `);
    float p3 = `+ String(Math.random()) + `*sin(iTime*0.02+`+ String(Math.random()*4) + `);

    float anim0000 = (1.) - (1.*p0*0. + 1.*p1*0. + 1.*p2*0. + 1.*p3*0.) + (1.*p0*0.*p1*0. + 1.*p0*0.*p2*0. + 1.*p0*0.*p3*0. + 1.*p1*0.*p2*0. + 1.*p1*0.*p3*0. + 1.*p2*0.*p3*0.) - (1.*p0*0.*p1*0.*p2*0. + 1.*p0*0.*p1*0.*p3*0. + 1.*p0*0.*p2*0.*p3*0. + 1.*p1*0.*p2*0.*p3*0.) + (1.*p0*0.*p1*0.*p2*0.*p3*0.);
    float anim0001 = (1.*p0*0. + 1.*p1*0. + 1.*p2*0. + 1.*p3*1.) - (1.*p0*0.*p1*0. + 1.*p0*0.*p2*0. + 1.*p0*0.*p3*1. + 1.*p1*0.*p2*0. + 1.*p1*0.*p3*1. + 1.*p2*0.*p3*1.) + (1.*p0*0.*p1*0.*p2*0. + 1.*p0*0.*p1*0.*p3*1. + 1.*p0*0.*p2*0.*p3*1. + 1.*p1*0.*p2*0.*p3*1.) - (1.*p0*0.*p1*0.*p2*0.*p3*1.);
    float anim0010 = (1.*p0*0. + 1.*p1*0. + 1.*p2*1. + 1.*p3*0.) - (1.*p0*0.*p1*0. + 1.*p0*0.*p2*1. + 1.*p0*0.*p3*0. + 1.*p1*0.*p2*1. + 1.*p1*0.*p3*0. + 1.*p2*1.*p3*0.) + (1.*p0*0.*p1*0.*p2*1. + 1.*p0*0.*p1*0.*p3*0. + 1.*p0*0.*p2*1.*p3*0. + 1.*p1*0.*p2*1.*p3*0.) - (1.*p0*0.*p1*0.*p2*1.*p3*0.);
    float anim0011 = (1.*p0*0.*p1*0. + 1.*p0*0.*p2*1. + 1.*p0*0.*p3*1. + 1.*p1*0.*p2*1. + 1.*p1*0.*p3*1. + 1.*p2*1.*p3*1.) - (1.*p0*0.*p1*0.*p2*1. + 1.*p0*0.*p1*0.*p3*1. + 1.*p0*0.*p2*1.*p3*1. + 1.*p1*0.*p2*1.*p3*1.) + (1.*p0*0.*p1*0.*p2*1.*p3*1.);
    float anim0100 = (1.*p0*0. + 1.*p1*1. + 1.*p2*0. + 1.*p3*0.) - (1.*p0*0.*p1*1. + 1.*p0*0.*p2*0. + 1.*p0*0.*p3*0. + 1.*p1*1.*p2*0. + 1.*p1*1.*p3*0. + 1.*p2*0.*p3*0.) + (1.*p0*0.*p1*1.*p2*0. + 1.*p0*0.*p1*1.*p3*0. + 1.*p0*0.*p2*0.*p3*0. + 1.*p1*1.*p2*0.*p3*0.) - (1.*p0*0.*p1*1.*p2*0.*p3*0.);
    float anim0101 = (1.*p0*0.*p1*1. + 1.*p0*0.*p2*0. + 1.*p0*0.*p3*1. + 1.*p1*1.*p2*0. + 1.*p1*1.*p3*1. + 1.*p2*0.*p3*1.) - (1.*p0*0.*p1*1.*p2*0. + 1.*p0*0.*p1*1.*p3*1. + 1.*p0*0.*p2*0.*p3*1. + 1.*p1*1.*p2*0.*p3*1.) + (1.*p0*0.*p1*1.*p2*0.*p3*1.);
    float anim0110 = (1.*p0*0.*p1*1. + 1.*p0*0.*p2*1. + 1.*p0*0.*p3*0. + 1.*p1*1.*p2*1. + 1.*p1*1.*p3*0. + 1.*p2*1.*p3*0.) - (1.*p0*0.*p1*1.*p2*1. + 1.*p0*0.*p1*1.*p3*0. + 1.*p0*0.*p2*1.*p3*0. + 1.*p1*1.*p2*1.*p3*0.) + (1.*p0*0.*p1*1.*p2*1.*p3*0.);
    float anim0111 = (1.*p0*0.*p1*1.*p2*1. + 1.*p0*0.*p1*1.*p3*1. + 1.*p0*0.*p2*1.*p3*1. + 1.*p1*1.*p2*1.*p3*1.) - (1.*p0*0.*p1*1.*p2*1.*p3*1.);
    float anim1000 = (1.*p0*1. + 1.*p1*0. + 1.*p2*0. + 1.*p3*0.) - (1.*p0*1.*p1*0. + 1.*p0*1.*p2*0. + 1.*p0*1.*p3*0. + 1.*p1*0.*p2*0. + 1.*p1*0.*p3*0. + 1.*p2*0.*p3*0.) + (1.*p0*1.*p1*0.*p2*0. + 1.*p0*1.*p1*0.*p3*0. + 1.*p0*1.*p2*0.*p3*0. + 1.*p1*0.*p2*0.*p3*0.) - (1.*p0*1.*p1*0.*p2*0.*p3*0.);
    float anim1001 = (1.*p0*1.*p1*0. + 1.*p0*1.*p2*0. + 1.*p0*1.*p3*1. + 1.*p1*0.*p2*0. + 1.*p1*0.*p3*1. + 1.*p2*0.*p3*1.) - (1.*p0*1.*p1*0.*p2*0. + 1.*p0*1.*p1*0.*p3*1. + 1.*p0*1.*p2*0.*p3*1. + 1.*p1*0.*p2*0.*p3*1.) + (1.*p0*1.*p1*0.*p2*0.*p3*1.);
    float anim1010 = (1.*p0*1.*p1*0. + 1.*p0*1.*p2*1. + 1.*p0*1.*p3*0. + 1.*p1*0.*p2*1. + 1.*p1*0.*p3*0. + 1.*p2*1.*p3*0.) - (1.*p0*1.*p1*0.*p2*1. + 1.*p0*1.*p1*0.*p3*0. + 1.*p0*1.*p2*1.*p3*0. + 1.*p1*0.*p2*1.*p3*0.) + (1.*p0*1.*p1*0.*p2*1.*p3*0.);
    float anim1011 = (1.*p0*1.*p1*0.*p2*1. + 1.*p0*1.*p1*0.*p3*1. + 1.*p0*1.*p2*1.*p3*1. + 1.*p1*0.*p2*1.*p3*1.) - (1.*p0*1.*p1*0.*p2*1.*p3*1.);
    float anim1100 = (1.*p0*1.*p1*1. + 1.*p0*1.*p2*0. + 1.*p0*1.*p3*0. + 1.*p1*1.*p2*0. + 1.*p1*1.*p3*0. + 1.*p2*0.*p3*0.) - (1.*p0*1.*p1*1.*p2*0. + 1.*p0*1.*p1*1.*p3*0. + 1.*p0*1.*p2*0.*p3*0. + 1.*p1*1.*p2*0.*p3*0.) + (1.*p0*1.*p1*1.*p2*0.*p3*0.);
    float anim1101 = (1.*p0*1.*p1*1.*p2*0. + 1.*p0*1.*p1*1.*p3*1. + 1.*p0*1.*p2*0.*p3*1. + 1.*p1*1.*p2*0.*p3*1.) - (1.*p0*1.*p1*1.*p2*0.*p3*1.);
    float anim1110 = (1.*p0*1.*p1*1.*p2*1. + 1.*p0*1.*p1*1.*p3*0. + 1.*p0*1.*p2*1.*p3*0. + 1.*p1*1.*p2*1.*p3*0.) - (1.*p0*1.*p1*1.*p2*1.*p3*0.);
    float anim1111 = (1.*p0*1.*p1*1.*p2*1.*p3*1.);

    
    for (int i=0; i<iter; i++) {

        z = 0.  + anim0000 * vec2(
            -0.20342348266472143 + ((-0.6552381801272968)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(-0.3594410511223629)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.1487811026900978)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(-0.6851767656990362)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            -0.9546207915060687 + ((-0.3594410511223629)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(-0.6552381801272968)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.6851767656990362)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(0.1487811026900978)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim0001 * vec2(
            0.3000227165947573 + ((-0.647676885129219)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.4595890691047757)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.6432219317209855)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(-0.34059556586010586)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            -0.21069468458927787 + ((0.4595890691047757)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(-0.647676885129219)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.34059556586010586)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(0.6432219317209855)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim0010 * vec2(
            0.17737752793284733 + ((0.8861129119361799)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.34825683871001933)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.3486022050792281)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(0.7427334759375572)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            0.5499611626088665 + ((0.34825683871001933)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.8861129119361799)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.7427334759375572)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.3486022050792281)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim0011 * vec2(
            -0.08974108699101624 + ((-0.7056572415666411)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(-0.5485229522676427)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.4127388614870029)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(0.5866683754216726)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            -0.6910498658177644 + ((-0.5485229522676427)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(-0.7056572415666411)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.5866683754216726)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.4127388614870029)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim0100 * vec2(
            0.6363559397286611 + ((0.9494665424029827)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(-0.5465896255825002)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.10465601068126906)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(-0.7001903658358388)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            0.946738391944111 + ((-0.5465896255825002)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.9494665424029827)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.7001903658358388)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.10465601068126906)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim0101 * vec2(
            -0.2526559391051759 + ((0.2109634062240513)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.25391858881743756)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.7124772733307936)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(0.6235134353607403)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            -0.10597435681747736 + ((0.25391858881743756)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.2109634062240513)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.6235134353607403)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.7124772733307936)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim0110 * vec2(
            0.3597195994095588 + ((0.03271266714757637)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.047391793289631945)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.7656211560739941)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(-0.9127702273522558)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            0.44353091920373267 + ((0.047391793289631945)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.03271266714757637)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.9127702273522558)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.7656211560739941)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim0111 * vec2(
            -0.4816146540893598 + ((-0.5195549377540327)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.7968062058652676)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.5731916868203726)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(-0.6879836246122184)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            -0.904131716552623 + ((0.7968062058652676)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(-0.5195549377540327)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.6879836246122184)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(0.5731916868203726)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim1000 * vec2(
            -0.32095664688084047 + ((-0.9236497230837932)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.8268437389259513)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.46731427098925704)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(-0.37327247948278197)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            0.5796632857062134 + ((0.8268437389259513)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(-0.9236497230837932)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.37327247948278197)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.46731427098925704)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim1001 * vec2(
            -0.31393286949985266 + ((0.24486854327699725)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.05051907869576899)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.5951440535224286)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(-0.6998559866083645)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            -0.9483063740761517 + ((0.05051907869576899)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.24486854327699725)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.6998559866083645)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.5951440535224286)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim1010 * vec2(
            0.9713100068211713 + ((0.2527065903085488)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.054229151988330226)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.8450830354470944)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(0.5274247589344199)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            -0.4622460340642969 + ((0.054229151988330226)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.2527065903085488)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.5274247589344199)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.8450830354470944)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim1011 * vec2(
            0.4510732823824306 + ((0.8728251349721015)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(-0.40212803379868856)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.34427286307900906)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(0.6378661663174567)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            -0.6046018379037961 + ((-0.40212803379868856)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.8728251349721015)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.6378661663174567)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.34427286307900906)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim1100 * vec2(
            -0.812448672309517 + ((-0.714678505031862)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.13714478766972538)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.2210074863514644)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(-0.43696347465067165)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            0.33506844214840537 + ((0.13714478766972538)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(-0.714678505031862)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.43696347465067165)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(0.2210074863514644)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim1101 * vec2(
            0.5770115037867136 + ((0.14727475901604214)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.7215210279375865)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.13937221519646315)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(0.5956516910783736)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            -0.6650102998110545 + ((0.7215210279375865)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.14727475901604214)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.5956516910783736)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.13937221519646315)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim1110 * vec2(
            0.04458003258212839 + ((0.7148692781413226)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.5132745458785333)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.20678039608765975)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(-0.5085169283315321)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            -0.8388758973188879 + ((0.5132745458785333)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.7148692781413226)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.5085169283315321)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(0.20678039608765975)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        ) + anim1111 * vec2(
            0.05390342596018849 + ((-0.05609770919125512)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(0.004580536578348227)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.893479058270912)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(0.1960849303032446)*(2.0*pow(z.x,1.)*pow(z.y,1.))),
            0.5952468729055918 + ((0.004580536578348227)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(-0.05609770919125512)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((0.1960849303032446)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.893479058270912)*(2.0*pow(z.x,1.)*pow(z.y,1.)))
        );
`
    ]


   // replace in with attribute and out with varying?
  const vs = `#version 300 es
  // an attribute is an input (in) to a vertex shader.
  // It will receive data from a buffer
  in vec4 a_position;

  // all shaders have a main function
  void main() {

    // gl_Position is a special variable a vertex shader
    // is responsible for setting
    gl_Position = a_position;
  }
  `;

  const fs = `#version 300 es
  precision highp float;
  uniform float iTime;
  uniform vec2 iResolution;
  uniform vec2 iMouse;
  uniform vec2 center;
  uniform float zoom_amount;
  uniform int colouring;
  uniform vec3 lp;
  uniform vec3 rp;
  uniform vec3 cmapc;
  uniform int iterParam;
  out vec4 fragColor;
  

  vec3 map(in float t)
  {
      vec3 rgb;
  
      // all colourings
      if (colouring == 1)
      {
          // At sea
          rgb = vec3(
          9.93*pow(t,3.8)*pow((1.-t),0.9),
          12.95*pow(t,2.8)*pow((1.-t),1.3),
          20.67*pow(t,1.8)*pow((1.-t),2.7)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
      else if (colouring == 2)
      {
          // Ice blue
          rgb = vec3(
          70.5*pow(t,4.7)*pow((1.-t),2.6),
          10.18*pow(t,2.8)*pow((1.-t),1.1),
          2.6*pow(t,0.8)*pow((1.-t),0.5)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
      else if (colouring == 3)
      {
          // Yellow and Purple
          rgb = vec3(
          1.68*pow(t,0.2)*pow((1.-t),0.9),
          42.35*pow(t,1.9)*pow((1.-t),4.1),
          4.61*pow(t,1.6)*pow((1.-t),0.8)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
      else if (colouring == 4)
      {
          // Earth
          rgb = vec3(
          5.76*pow(t,0.7)*pow((1.-t),2.8),
          6.49*pow(t,1.3)*pow((1.-t),1.4),
          exp(-9.*pow(t-0.8,2.))
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float(t>=0.));
          //
      }
      else if (colouring == 5)
      {
          // Cyan and Magenta decay
          rgb = vec3(
          2.*exp(-10.*pow(t-0.2,2.))*pow(t,0.6),
          exp(-20.*pow(t-0.7,2.)),
          exp(-5.*pow(t-0.5,2.))
          );
          rgb = vec3(rgb.x,rgb.y,rgb.z);
          //
      }
      else if (colouring == 6)
      {
          // Emergency exit
          rgb = vec3(
          1.68*pow(t,0.2)*pow((1.-t),0.9)*(1.-pow((sin(iTime*2.)+1.)/2.,3.)),
          12.06*pow(t,1.9)*pow((1.-t),1.7),
          1.61*pow(t,1.6)*pow((1.-t),0.8)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
      else if (colouring == 7)
      {
          // Inverted lightness RGB
          rgb = vec3(
          t+0.2*sin(iTime*0.1)-0.2,
          t+0.2*sin(2.+iTime*0.1)-0.2,
          t+0.2*sin(3.+iTime*0.1)-0.2
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.))+float(t>=1.),rgb.y*float((0.<=t)&&(t<=1.))+float(t>=1.),rgb.z*float((0.<=t)&&(t<=1.))+float(t>=1.));
          //
      }
      else if (colouring == 8)
      {
          // Literature
          rgb = vec3(
          7.79*pow(t,1.7)*pow((1.-t),1.3),
          10.18*pow(t,2.8)*pow((1.-t),1.1),
          50.9*pow(t,1.8)*pow((1.-t),5.0)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
          else if (colouring == -1)
      {
          // Literature
          rgb = vec3(
          cmapc.r*pow(t,lp.r)*pow((1.-t),rp.r),
          cmapc.g*pow(t,lp.g)*pow((1.-t),rp.g),
          cmapc.b*pow(t,lp.b)*pow((1.-t),rp.b)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
  
      else
      
      {
          // Default (0)
          rgb = vec3(
          17.484430816275246*pow(t,4.362884336095945)*pow((1.-t),1.1738002744885567),
          5.167710066164584*pow(t,1.33361222833035)*pow((1.-t),1.0584944073735307),
          311.16840825145783*pow(t,4.678644031269574)*pow((1.-t),3.6863406789220625)
          );
          rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
          //
      }
          
  
      return rgb;
  
  }
  
  
  void main( ) {
  
    vec2 uv = vec2(fract(gl_FragCoord.xy / iResolution));
    vec2 fragCoord = uv*iResolution.xy; // this creates an equivalent to ShaderToy's fragCoord variable
    vec2 new_uv = (fragCoord*2. - iResolution.xy)/iResolution.y; // centered

    //vec2 fragCoord = gl_FragCoord.xy;

    vec2 z = new_uv*zoom_amount+center;
    //float gr = 0.65+sin(iTime*0.01)*0.05; //varying circle radii
    //vec2 c = vec2(cos(iTime*0.04), sin(iTime*0.04))*gr; // complex variable c going in circles around origin
    
    // fixed
    vec2 c = vec2(-0.8,0.156);
    //vec2 c = vec2(((iMouse.x/iResolution.x)*2.-1.)*2.*zoom_amount*(iResolution.x/(2.*iResolution.y))-center.x, ((-(iMouse.y/iResolution.y)+1.)*2.-1.)*zoom_amount)-center.y;
    //vec2 c = vec2(-0.945, -0.275);
    //vec2 c = vec2(1.008,0.2472);

    /*
        Compute iter iterates of f on the rendered complex plane
        z.x should always be overwritten to real part of f(z),
        z.y should always be overwritten to imaginary part of f(z).
    */

    //int iter = int(iTime*10.);
    int iter = iterParam;


    vec2 check = (z/z)*2.; // constant that's the same size as z, to allow use of lessThan function
    vec2 esc = check*float(iter/2); // escape uv
    ` + 
    funcs[Math.round(Math.random()*(Math.round(funcs.length)-0.5))] + `

        esc -= vec2(lessThan(z,check)); // does not work as intended as big values aren't "bigger", just undefined
    }

    esc /= float(iter); // esc values are between 0 and iter, so they need to be normalized

    float zmod = sqrt(z.x*z.x + z.y*z.y);
    float angle = atan(z.y/z.x);
    
    // smooth colouring using modified Bernstein equations
    float t = length(esc);
    vec3 RGB = map(t);
    //vec3 RGB = vec3(zmod, angle, angle);

    // iMouse.x/iResolution.x //
    // iMouse.y/iResolution.y //
    // how close the mouse is to the right / bottom edge of the screen between [0,1]

    // RGB = RGB + hsl2rgb(vec3(angle, 0.3, zmod));

    fragColor = vec4(RGB, 1.0);


}
  `;

  // setup GLSL program
  const program = webglUtils.createProgramFromSources(gl, [vs, fs]);

  // look up where the vertex data needs to go.
  const positionAttributeLocation = gl.getAttribLocation(program, "a_position");

  // look up uniform locations
  const resolutionLocation = gl.getUniformLocation(program, "iResolution");
  const mouseLocation = gl.getUniformLocation(program, "iMouse");
  const timeLocation = gl.getUniformLocation(program, "iTime");
  const centerLocation = gl.getUniformLocation(program, "center");
  const zoomamountLocation = gl.getUniformLocation(program, "zoom_amount");
  const iterParamLocation = gl.getUniformLocation(program, "iterParam");
  
  const colouringLocation = gl.getUniformLocation(program, "colouring");
  const cmapcLocation = gl.getUniformLocation(program, "cmapc");
  const lpLocation = gl.getUniformLocation(program, "lp");
  const rpLocation = gl.getUniformLocation(program, "rp");
  
  
  
  

  // Create a vertex array object (attribute state)
  const vao = gl.createVertexArray();

  // and make it the one we're currently working with
  gl.bindVertexArray(vao);

  // Create a buffer to put three 2d clip space points in
  const positionBuffer = gl.createBuffer();

  // Bind it to ARRAY_BUFFER (think of it as ARRAY_BUFFER = positionBuffer)
  gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

  // fill it with a 2 triangles that cover clip space
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([
    -1, -1,  // first triangle
     1, -1,
    -1,  1,
    -1,  1,  // second triangle
     1, -1,
     1,  1,
  ]), gl.STATIC_DRAW);

  // Turn on the attribute
  gl.enableVertexAttribArray(positionAttributeLocation);

  // Tell the attribute how to get data out of positionBuffer (ARRAY_BUFFER)
  gl.vertexAttribPointer(
      positionAttributeLocation,
      2,          // 2 components per iteration
      gl.FLOAT,   // the data is 32bit floats
      false,      // don't normalize the data
      0,          // 0 = move forward size * sizeof(type) each iteration to get the next position
      0,          // start at the beginning of the buffer
  );

  let mouseX = 0;
  let mouseY = 0;

  function setMousePosition(e) {
    const rect = canvas.getBoundingClientRect();
    mouseX = e.clientX - rect.left;
    mouseY = rect.height - (e.clientY - rect.top) - 1;  // bottom is 0 in WebGL
  }

  canvas.addEventListener('mousemove', setMousePosition);
  canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
  }, {passive: false});
  canvas.addEventListener('touchmove', (e) => {
    e.preventDefault();
    setMousePosition(e.touches[0]);
  }, {passive: false});

  function render(time) {
    time *= 0.001;  // convert to seconds

    webglUtils.resizeCanvasToDisplaySize(gl.canvas);

    // Tell WebGL how to convert from clip space to pixels
    gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);

    // Tell it to use our program (pair of shaders)
    gl.useProgram(program);

    // Bind the attribute/buffer set we want.
    gl.bindVertexArray(vao);

    gl.uniform2f(resolutionLocation, gl.canvas.width, gl.canvas.height);
    gl.uniform2f(mouseLocation, mouseX, mouseY);
    gl.uniform2f(centerLocation, parseFloat(document.getElementById("#centerX").innerHTML), parseFloat(document.getElementById("#centerY").innerHTML));
    gl.uniform1f(timeLocation, time);
    gl.uniform1i(iterParamLocation, parseInt(document.getElementById("#iterParam").innerHTML));
    gl.uniform1f(zoomamountLocation, parseFloat(document.getElementById("#zoom_amount").innerHTML));
    gl.uniform1i(colouringLocation, parseInt(document.getElementById("#colouring").innerHTML));
    gl.uniform3f(cmapcLocation, parseFloat(document.getElementById("#cmapcR").innerHTML), parseFloat(document.getElementById("#cmapcG").innerHTML), parseFloat(document.getElementById("#cmapcB").innerHTML));
    gl.uniform3f(lpLocation, parseFloat(document.getElementById("#lpR").innerHTML), parseFloat(document.getElementById("#lpG").innerHTML), parseFloat(document.getElementById("#lpB").innerHTML));
    gl.uniform3f(rpLocation, parseFloat(document.getElementById("#rpR").innerHTML), parseFloat(document.getElementById("#rpG").innerHTML), parseFloat(document.getElementById("#rpB").innerHTML));
    
    

    gl.drawArrays(
        gl.TRIANGLES,
        0,     // offset
        6,     // num vertices to process
    );

    requestAnimationFrame(render);
    
  }
  
  requestAnimationFrame(render);

  


}


main();
