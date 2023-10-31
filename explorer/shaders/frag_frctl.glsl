#version 330 core
in vec2 uv;
uniform float iTime;
uniform vec2 iResolution;
uniform vec2 iMouse;
uniform vec2 center;
uniform float zoom_amount;
uniform int colouring;
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
        2*exp(-10.*pow(t-0.2,2.))*pow(t,0.6),
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
        1.68*pow(t,0.2)*pow((1.-t),0.9)*(1-pow((sin(iTime*2.)+1.)/2.,3.)),
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

    else
    
    {
        // Default (0)
        rgb = vec3(
        4.115471913683428*pow(t,1.881953076949107)*pow((1.-t),0.6298242975265675),
        63.90893891041876*pow(t,4.681529575609478)*pow((1.-t),2.0667429499400427),
        7.149916617986545*pow(t,1.1354316325952278)*pow((1.-t),1.8169024464075525)
        );
        rgb = vec3(rgb.x*float((0.<=t)&&(t<=1.)),rgb.y*float((0.<=t)&&(t<=1.)),rgb.z*float((0.<=t)&&(t<=1.)));
        //
    }
        

    return rgb;

}


vec3 hsl2rgb( in vec3 c )
{
    vec3 rgb = clamp( abs(mod(c.x*6.0+vec3(0.0,4.0,2.0),6.0)-3.0)-1.0, 0.0, 1.0 );

    return c.z + c.y * (rgb-0.5)*(1.0-abs(2.0*c.z-1.0));
}

void main( )
{
    vec2 fragCoord = uv*iResolution.xy; // this creates an equivalent to ShaderToy's fragCoord variable
    vec2 new_uv = (fragCoord*2. - iResolution.xy)/iResolution.y; // centered


    vec2 z = new_uv*zoom_amount+center;
    //float gr = 0.65+sin(iTime*0.01)*0.05; //varying circle radii
    //vec2 c = vec2(cos(iTime*0.04), sin(iTime*0.04))*gr; // complex variable c going in circles around origin
    
    // fixed
    vec2 c = vec2(0.,0.);
    //vec2 c = vec2(((iMouse.x/iResolution.x)*2.-1.)*2*zoom_amount*(iResolution.x/(2.*iResolution.y))-center.x, ((-(iMouse.y/iResolution.y)+1.)*2.-1.)*zoom_amount)-center.y;

    /*
        Compute iter iterates of f on the rendered complex plane
        z.x should always be overwritten to real part of f(z),
        z.y should always be overwritten to imaginary part of f(z).
    */

    int iter = int(iTime*10.);
    //int iter = 200;


    vec2 check = (z/z)*2.; // constant that's the same size as z, to allow use of lessThan function
    vec2 esc = check*iter/2; // escape uv
    
    for (int i=0; i<iter; i++) {

        z = vec2(
            0.49737205770970405 + ((0.3925862909958151)*(1.0*pow(z.x,1.)*pow(z.y,0.))-(-0.3358032529299304)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.5106388496704075)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))-(-0.8137798641631115)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((0.13504580488318307)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))-(-0.9542561166666934)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))) + ((-0.09780454226043656)*(1.0*pow(z.x,0.)*pow(z.y,4.) - 6.0*pow(z.x,2.)*pow(z.y,2.) + 1.0*pow(z.x,4.)*pow(z.y,0.))-(0.22830049679715136)*( - 4.0*pow(z.x,1.)*pow(z.y,3.) + 4.0*pow(z.x,3.)*pow(z.y,1.))) + ((0.8801510036449425)*(5.0*pow(z.x,1.)*pow(z.y,4.) - 10.0*pow(z.x,3.)*pow(z.y,2.) + 1.0*pow(z.x,5.)*pow(z.y,0.))-(-0.048691229839912475)*(1.0*pow(z.x,0.)*pow(z.y,5.) - 10.0*pow(z.x,2.)*pow(z.y,3.) + 5.0*pow(z.x,4.)*pow(z.y,1.))),
            -0.5558426928777755 + ((-0.3358032529299304)*(1.0*pow(z.x,1.)*pow(z.y,0.))+(0.3925862909958151)*(1.0*pow(z.x,0.)*pow(z.y,1.))) + ((-0.8137798641631115)*( - 1.0*pow(z.x,0.)*pow(z.y,2.) + 1.0*pow(z.x,2.)*pow(z.y,0.))+(-0.5106388496704075)*(2.0*pow(z.x,1.)*pow(z.y,1.))) + ((-0.9542561166666934)*( - 3.0*pow(z.x,1.)*pow(z.y,2.) + 1.0*pow(z.x,3.)*pow(z.y,0.))+(0.13504580488318307)*( - 1.0*pow(z.x,0.)*pow(z.y,3.) + 3.0*pow(z.x,2.)*pow(z.y,1.))) + ((0.22830049679715136)*(1.0*pow(z.x,0.)*pow(z.y,4.) - 6.0*pow(z.x,2.)*pow(z.y,2.) + 1.0*pow(z.x,4.)*pow(z.y,0.))+(-0.09780454226043656)*( - 4.0*pow(z.x,1.)*pow(z.y,3.) + 4.0*pow(z.x,3.)*pow(z.y,1.))) + ((-0.048691229839912475)*(5.0*pow(z.x,1.)*pow(z.y,4.) - 10.0*pow(z.x,3.)*pow(z.y,2.) + 1.0*pow(z.x,5.)*pow(z.y,0.))+(0.8801510036449425)*(1.0*pow(z.x,0.)*pow(z.y,5.) - 10.0*pow(z.x,2.)*pow(z.y,3.) + 5.0*pow(z.x,4.)*pow(z.y,1.)))
        );


        esc -= vec2(lessThan(z,check)); // does not work as intended as big values aren't "bigger", just undefined
    }

    esc /= iter; // esc values are between 0 and iter, so they need to be normalized

    float zmod = sqrt(z.x*z.x + z.y*z.y);
    float angle = atan(z.y/z.x);
    
    // smooth colouring using modified Bernstein equations
    float t = length(esc);
    vec3 RGB = map(t);

    // iMouse.x/iResolution.x //
    // iMouse.y/iResolution.y //
    // how close the mouse is to the right / bottom edge of the screen between [0,1]

    // RGB = RGB + hsl2rgb(vec3(angle, 0.3, zmod));

    fragColor = vec4(RGB, 1.0);


}