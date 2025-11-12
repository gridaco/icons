export const GridaLogo = ({
  className,
  ...props
}: React.ComponentProps<"svg">) => {
  return (
    <svg
      width="24"
      height="24"
      viewBox="0 0 42 42"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      {...props}
    >
      <path
        fill="currentColor"
        d="m27.658 13.869-.078 14.42L41.527 41.92v-14.42l-.002-.002c-.127-7.55-6.287-13.63-13.867-13.63ZM26.02 7.179c-6.925.775-12.309 6.65-12.309 13.782v6.619L13.947 42 0 28.368V13.79C.043 6.167 6.235 0 13.87 0c5.233 0 9.79 2.899 12.151 7.179Z"
      />
    </svg>
  );
};
